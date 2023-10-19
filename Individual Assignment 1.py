# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 17:58:46 2023

@author: donna
"""
import gurobipy as gp
from gurobipy import GRB
from gurobipy import *

model = gp.Model ('AssignmentQ1_2023_final')

# ---- Parameters ----

products        = ['airfryer', 'breadmaker', 'coffeemaker']
operationsteps  = ['molding', 'assembling', 'finishing', 'packaging']
months          = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']    

holdingcosts_finished   = {                       # euro / product
    'airfryer'    : 800e-3,
    'breadmaker'  : 1500e-3,
    'coffeemaker' : 500e-3
    }

holdingcosts_packaged   = {                       # euro / product
    'airfryer'    : 1000e-3,
    'breadmaker'  : 1000e-3,
    'coffeemaker' : 1000e-3
    }

capacity = {
    'molding'     : 80,                           # hour
    'assembling'  : 100,
    'finishing'   : 100,
    'packaging'   : 250
    }

T_po = {                                # hour / product
    ('airfryer', 'molding'): 0.6e-3,
    ('breadmaker', 'molding'): 1.2e-3,
    ('coffeemaker', 'molding'): 0.5e-3,
    ('airfryer', 'assembling'): 0.8e-3,
    ('breadmaker', 'assembling'): 0.5e-3,
    ('coffeemaker', 'assembling'): 0.1e-3,
    ('airfryer', 'finishing'): 0.1e-3,
    ('breadmaker', 'finishing'): 2.0e-3,
    ('coffeemaker', 'finishing'): 0.1e-3,
    ('airfryer', 'packaging'): 2.5e-3,
    ('breadmaker', 'packaging'): 2.5e-3,
    ('coffeemaker', 'packaging'): 2.5e-3
}                   

D_mp = {                                        # product
    ('Jan', 'airfryer')     : 10e3,
    ('Jan', 'breadmaker')   : 11e3,
    ('Jan', 'coffeemaker')  : 10e3,
    ('Feb', 'airfryer')     : 20e3,
    ('Feb', 'breadmaker')   : 13e3,
    ('Feb', 'coffeemaker')  : 20e3,
    ('Mar', 'airfryer')     : 25e3,
    ('Mar', 'breadmaker')   : 12e3,
    ('Mar', 'coffeemaker')  : 50e3,
    ('Apr', 'airfryer')     : 30e3,
    ('Apr', 'breadmaker')   : 11e3,
    ('Apr', 'coffeemaker')  : 10e3,
    ('May', 'airfryer')     : 50e3,
    ('May', 'breadmaker')   : 10e3,
    ('May', 'coffeemaker')  : 20e3,
    ('June', 'airfryer')    : 70e3,
    ('June', 'breadmaker')  : 10e3,
    ('June', 'coffeemaker') : 50e3,
    ('July', 'airfryer')    : 10e3,
    ('July', 'breadmaker')  : 10e3,
    ('July', 'coffeemaker') : 10e3,
    ('Aug', 'airfryer')     : 12e3,
    ('Aug', 'breadmaker')   : 12e3,
    ('Aug', 'coffeemaker')  : 20e3,
    ('Sep', 'airfryer')     : 10e3,
    ('Sep', 'breadmaker')   : 11e3,
    ('Sep', 'coffeemaker')  : 50e3,
    ('Oct', 'airfryer')     : 300.2e3,
    ('Oct', 'breadmaker')   : 10e3,
    ('Oct', 'coffeemaker')  : 10e3,
    ('Nov', 'airfryer')     : 20.0e3,
    ('Nov', 'breadmaker')   : 50.4e3,
    ('Nov', 'coffeemaker')  : 20.0e3,
    ('Dec', 'airfryer')     : 14.8e3,
    ('Dec', 'breadmaker')   : 10.6e3,
    ('Dec', 'coffeemaker')  : 55.5e3
    }

# ---- Sets ----
#M = range (len (months))             # set of months
#P = range (len (products) )          # set of product types
#O = range (len (operationsteps) )   # set of operationsteps

# ---- Variables ----

X_mp = model.addVars(months, products, lb = 0, vtype=GRB.INTEGER, name="X_mp") # quantity produced products
Y_mp = model.addVars(months, products, lb = 0, vtype=GRB.INTEGER, name="Y_mp") # quantity stored after finishing
Z_mp = model.addVars(months, products, lb = 0, vtype=GRB.INTEGER, name="Z_mp") # quantity stored after packaging
I_mp = model.addVars(months, products, lb = 0, vtype=GRB.INTEGER, name="I_mp") # inventory of stored products

model.update ()
# ---- Constraints ----

# Constraints 1: production and storage meeting demand
for m in months:
    for p in products:
        model.addConstr(X_mp[m, p] + Z_mp[m, p] + I_mp[m, p] >= D_mp[m, p], f"D_mp_{m}_{p}")

# Constraints 2: maximum capacity
for m in months:
    for o in operationsteps:
        model.addConstr((gp.quicksum(T_po[p, o] * X_mp[m, p] for p in products)) <= capacity[o] , f"Capacity_{m}_{o}")

#Constraint 3: amount of stored products for m = 0
for p in products:
    model.addConstr(Z_mp[months[0], p] == (X_mp[months[0], p] - Y_mp[months[0], p]), f"Z_{m}_{p}")
        
# Constraints 4: amount of stored products
for i, m in enumerate(months[1:]):
    for p in products:
        model.addConstr(Z_mp[months[i], p] == (Y_mp[months[i-1], p] + X_mp[months[i], p] - Y_mp[months[i], p]), f"Z_{m}_{p}")

# Constraints 5: inventory packaged products
for m in months:
    for p in products:
        model.addConstr(I_mp[m, p] == (Z_mp[m, p] - D_mp[m, p]), f"I_mp_{m}_{p}")

# Constraints 6: finished can not be more than produced
for m in months:
    for p in products:
        model.addConstr(Y_mp[m, p] <= X_mp[m, p])
        
        
# ---- Objective Function ----        
obj = gp.quicksum(holdingcosts_finished[p] * Y_mp[m, p] +  holdingcosts_packaged[p] * I_mp[m, p] for m in months for p in products)
model.setObjective(obj, GRB.MINIMIZE)
        
model.optimize()    
        


# finding out where the errors are
if model.Status == GRB.INFEASIBLE:
    model.computeIIS()
    
model.write('iismodel.ilp')

# Print out the IIS constraints and variables
print('\nThe following constraints and variables are in the IIS:')
for c in model.getConstrs():
    if c.IISConstr: print(f'\t{c.constrname}: {model.getRow(c)} {c.Sense} {c.RHS}')

for v in model.getVars():
    if v.IISLB: print(f'\t{v.varname} ≥ {v.LB}')
    if v.IISUB: print(f'\t{v.varname} ≤ {v.UB}')
        
        
        
        

