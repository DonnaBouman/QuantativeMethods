# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 17:58:46 2023

@author: donna
"""

from gurobipy import *

model = Model ('AssignmentQ1_2023_final')

# ---- Parameters ----

# Product characteristics
productname             = ('airfryer', 'breadmaker', 'coffeemaker')
holdingcosts_finished   = ( 800, 1500,  500)        # euro / 1000 products
holdingcosts_packaged   = (1000, 1000, 1000)        # euro / 1000 products

# Production process characteristics
productionstep              = ('molding', 'assembling', 'finishing', 'packaging')
productiontime_airfryer     = (0.6, 0.8, 0.1, 2.5)  # hour / 1000 products
productiontime_breadmaker   = (1.2, 0.5, 2.0, 2.5)  # hour / 1000 products
productiontime_coffeemaker  = (0.5, 0.1, 0.1, 2.5)  # hour / 1000 products
capacity                    = ( 80, 100, 100, 250)  # hour

# Expected demand characteristics
month               = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
#demand_airfryer     = (10, 20, 25, 30, 50, 70, 10, 12, 10, 300.2, 20.0, 14.8)   # 1000 products
#demand_breadmaker   = (11, 13, 12, 11, 10, 10, 10, 12, 11,  10.0, 50.4, 10.6)   # 1000 products
#demand_coffeemaker  = (10, 20, 50, 10, 20, 50, 10, 20, 50,  10.0, 20.0, 55.5)   # 1000 products

demand = {(10, 20, 25, 30, 50, 70, 10, 12, 10, 300.2, 20.0, 14.8), 
          (11, 13, 12, 11, 10, 10, 10, 12, 11,  10.0, 50.4, 10.6),
          (10, 20, 50, 10, 20, 50, 10, 20, 50,  10.0, 20.0, 55.5)
    }

# ---- Sets ----
M = range (len (month))                       # set of months
P = range (len (productname) )                # set of product types
O = range (len (productionstep) )             # set of operation steps

# ---- Variables ----
x1 = {} 
for m in M:
    for p in P:
        for o in range(1,4):
#            if productionstep != 'packaging':
#               x[m,p,o] = model.addVar (lb = 0, vtype = GRB.CONTINUOUS, obj = cargoprofit[i], name = 'X[' + str(m) + ',' + str(p) + ',' + str(o) + ']')
            x1[m,p,o] = model.addVar (lb = 0, vtype = GRB.CONTINUOUS, name = 'X1[' + str(m) + ',' + str(p) + ',' + str(o) + ']')

x2 = {} 
for m in M:
    for p in P:
        for o in O:
#            if productionstep == 'packaging':
#               x[m,p,o] = model.addVar (lb = 0, vtype = GRB.CONTINUOUS, obj = cargoprofit[i], name = 'X[' + str(m) + ',' + str(p) + ',' + str(o) + ']')
            x2[m,p,o] = model.addVar (lb = 0, vtype = GRB.CONTINUOUS, name = 'X2[' + str(m) + ',' + str(p) + ',' + str(o) + ']')

y1 = {} 
for m in M:
    for p in P:
        for o in O:
#            if productionstep == 'finishing':
#               x[m,p,o] = model.addVar (lb = 0, vtype = GRB.CONTINUOUS, obj = cargoprofit[i], name = 'X[' + str(m) + ',' + str(p) + ',' + str(o) + ']')
            y1[m,p,o] = model.addVar (lb = 0, vtype = GRB.CONTINUOUS, name = 'Y1[' + str(m) + ',' + str(p) + ',' + str(o) + ']')

y2 = {} 
for m in M:
    for p in P:
        for o in O:
#            if productionstep == 'packaging':
#               x[m,p,o] = model.addVar (lb = 0, vtype = GRB.CONTINUOUS, obj = cargoprofit[i], name = 'X[' + str(m) + ',' + str(p) + ',' + str(o) + ']')
            y2[m,p,o] = model.addVar (lb = 0, vtype = GRB.CONTINUOUS, name = 'Y2[' + str(m) + ',' + str(p) + ',' + str(o) + ']')

# Integrate new variables
model.update ()

# ---- Objective Function ----
#model.setObjective (quicksum (cargoprofit[i] * x[i,j] for m in M for p in P for o in O) )
model.setObjective (quicksum ((holdingcosts_finished[p] * y1[m,p,o]) + (holdingcosts_packaged[p] * y2[m,p,o]) for m in M for p in P for o in O) )
model.modelSense = GRB.MINIMIZE
model.update ()


# ---- Constraints ----
# Constraints 1: expected demand
con1 = {}
for m in M:
    for p in P:
        con1[m,p] = model.addConstr(quicksum (x2[m,p,o] + y2[m,p,o] for o in O) >= demand[m])
        
    #    con1[j] = model.addConstr( quicksum (cargovolume[i] * x[i,j] for i in I) <= maxvolume[j], 'con1[' + str(j) + ']-')



# Constraints 2: production capacity
con2 = {}

# Constraints 3: packaged products inventory
con3 = {}

# Constraints 4: finished products inventory
con4 = {}

# Constraints 5: non-negativity
con5 = {}


# ---- Solve ----



# --- Print results ---

