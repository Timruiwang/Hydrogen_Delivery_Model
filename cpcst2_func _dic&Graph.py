# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 15:55:55 2023

@author: wry19
"""

import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from cost_functions import calc_costs

D = 600   #600
DT = 20000   #6000

results = calc_costs(D, DT)
COST_LH_TRUCK_CAPEX = results["COST_LH_TRUCK_CAPEX"]
COST_GH_TRUCK_CAPEX = results["COST_GH_TRUCK_CAPEX"]
COST_GH_PIPE_CAPEX = results["COST_GH_PIPE_CAPEX"]
COST_LH_TRUCK_LAB = results["COST_LH_TRUCK_LAB"]
COST_GH_TRUCK_LAB = results["COST_GH_TRUCK_LAB"]
COST_GH_PIPE_OPEX = results["COST_GH_PIPE_OPEX"]
COST_LH_TRUCK_FRE = results["COST_LH_TRUCK_FRE"]
COST_GH_TRUCK_FRE = results["COST_GH_TRUCK_FRE"]
COST_GH_PIPE_FRE = results["COST_GH_PIPE_FRE"]
COST_LH_TRUCK_ELEC = results["COST_LH_TRUCK_ELEC"]
COST_GH_TRUCK_ELEC = results["COST_GH_TRUCK_ELEC"]
COST_GH_PIPE_ELEC = results["COST_GH_PIPE_ELEC"]
UNIT_LH_TRUCK = results["UNIT_LH_TRUCK"]
UNIT_GH_TRUCK = results["UNIT_GH_TRUCK"]
UNIT_GH_PIPE = results["UNIT_GH_PIPE"]
Emission_LH_TRUCK = results["Emission_LH_TRUCK"]
Emission_GH_TRUCK = results["Emission_GH_TRUCK"]
Emission_GH_PIPE = results["Emission_GH_PIPE"]
Emission_LH_TRUCK_OPEX = results["Emission_LH_TRUCK_OPEX"]
Emission_GH_TRUCK_OPEX = results["Emission_GH_TRUCK_OPEX"]
Emission_GH_PIPE_OPEX = results["Emission_GH_PIPE_OPEX"]
Emission_LH_TRUCK_CAPEX = results["Emission_LH_TRUCK_CAPEX"]
Emission_GH_TRUCK_CAPEX = results["Emission_GH_TRUCK_CAPEX"]
Emission_GH_PIPE_CAPEX = results["Emission_GH_PIPE_CAPEX"]
f = results["f"]

import matplotlib.pyplot as plt
import numpy as np
species = (
    f"LH Truck\n cost={UNIT_LH_TRUCK:.2E}\$",
    f"GH Truck\n cost={UNIT_GH_TRUCK:.2E}\$",
    f"GH Pipe\n cost={UNIT_GH_PIPE:.2E}\$",
)

weight_counts = {
    "CAPEX": np.array([COST_LH_TRUCK_CAPEX, COST_GH_TRUCK_CAPEX, COST_GH_PIPE_CAPEX])/f,
    "Labor cost": np.array([COST_LH_TRUCK_LAB,COST_GH_TRUCK_LAB,COST_GH_PIPE_OPEX])/f,
    "Fre cost": np.array([COST_LH_TRUCK_FRE, COST_GH_TRUCK_FRE, COST_GH_PIPE_FRE])/f,
    "Electricity cost": np.array([COST_LH_TRUCK_ELEC,COST_GH_TRUCK_ELEC,COST_GH_PIPE_ELEC])/f
}
width = 0.5

fig, ax = plt.subplots()
bottom = np.zeros(3)

for boolean, weight_count in weight_counts.items():
    p = ax.bar(species, weight_count, width, label=boolean, bottom=bottom)
    bottom += weight_count

ax.set_title("Transportation Cost /kg H2")
ax.legend(loc="upper right")

plt.show()

#%%

species = (
    f"LH Truck\n CO2={Emission_LH_TRUCK:.2E}\$",
    f"GH Truck\n cost={Emission_GH_TRUCK:.2E}\$",
    f"GH Pipe\n cost={Emission_GH_PIPE:.2E}\$",
)
weight_counts = {
    "CAPEX_Emission": np.array([Emission_LH_TRUCK_CAPEX, Emission_GH_TRUCK_CAPEX, Emission_GH_PIPE_CAPEX])/f,
    "OPEX_Emission": np.array([Emission_LH_TRUCK_OPEX, Emission_GH_TRUCK_OPEX, Emission_GH_PIPE_OPEX])/f,
}
width = 0.5

fig, ax = plt.subplots()
bottom = np.zeros(3)

for boolean, weight_count in weight_counts.items():
    p = ax.bar(species, weight_count, width, label=boolean, bottom=bottom)
    bottom += weight_count

ax.set_title("Transportation Emission /kg H2")
ax.legend(loc="upper right")



plt.show()

#%%Emission OPEX only
#%%

species = (
    f"LH Truck\n CO2={Emission_LH_TRUCK:.2E}\$",
    f"GH Truck\n cost={Emission_GH_TRUCK:.2E}\$",
    f"GH Pipe\n cost={Emission_GH_PIPE:.2E}\$",
)
weight_counts = {
    "OPEX_Emission": np.array([Emission_LH_TRUCK_OPEX, Emission_GH_TRUCK_OPEX, Emission_GH_PIPE_OPEX])/f,
}

width = 0.5

fig, ax = plt.subplots()
bottom = np.zeros(3)

for boolean, weight_count in weight_counts.items():
    p = ax.bar(species, weight_count, width, label=boolean, bottom=bottom)
    bottom += weight_count

ax.set_title("Transportation Emission")
ax.legend(loc="upper right")

plt.show()


#%%
SUM_LH_TRUCK = {}
SUM_GH_TRUCK = {}
SUM_GH_PIPE = {}
DT_x = {}

Ds = []
DTs = []
LHTs = []
GHTs = []
GHPs = []
ELHTs = []
EGHTs = []
EGHPs = []



from tqdm import tqdm
for D in tqdm(range(1, 300, 1)):
    Ds.append([])
    DTs.append([])
    LHTs.append([])
    GHTs.append([])
    GHPs.append([])
    ELHTs.append([])
    EGHTs.append([])
    EGHPs.append([])
    for DT in range(1, int(6e8), int(1e5)):
        out = calc_costs(D, DT)

        Ds[-1].append(D)
        DTs[-1].append(DT)
        LHTs[-1].append(out["UNIT_LH_TRUCK"])
        GHTs[-1].append(out["UNIT_GH_TRUCK"])
        GHPs[-1].append(out["UNIT_GH_PIPE"])
        ELHTs[-1].append(out["UNIT_Emission_LH_TRUCK"])
        EGHTs[-1].append(out["UNIT_Emission_GH_TRUCK"])
        EGHPs[-1].append(out["UNIT_Emission_GH_PIPE"])


import numpy as np

npDs = np.array(Ds)
npDTs = np.array(DTs)
npLHTs = np.array(LHTs)
npGHTs = np.array(GHTs)
npGHPs = np.array(GHPs)
npELHTs = np.array(ELHTs)
npEGHTs = np.array(EGHTs)
npEGHPs = np.array(EGHPs)


# from matplotlib import cm
# from matplotlib.ticker import LinearLocator
# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# ax.scatter(npDs, npDTs, npGHTs, linewidth=0, color='green',label='GasHydrogenTruck')
# ax.scatter(npDs, npDTs, npGHPs, linewidth=0, color='blue',label='LiquidHydrogenTruck')
# ax.scatter(npDs, npDTs, npLHTs, linewidth=0, color='red',label='GasPipeline')
# # ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter('{x:.0e}')
# # ax.set_zlim(0, 1e11)
# plt.savefig(f'costmatplot2.png', dpi=1200)
# plt.show()
# ax.legend()


# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# ax.scatter(npDs, npDTs, npEGHTs, linewidth=0, color='green',label='GasHydrogenTruck')
# ax.scatter(npDs, npDTs, npEGHPs, linewidth=0, color='blue',label='LiquidHydrogenTruck')
# ax.scatter(npDs, npDTs, npELHTs, linewidth=0, color='red',label='GasPipeline')
# # ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter('{x:.0e}')
# # ax.set_zlim(0, 1e11)
# plt.savefig(f'emimatplot2.png', dpi=1200)
# plt.show()
# ax.legend()


from mayavi import mlab


# In[5]:


mlab.mesh(np.log(npDs), np.log(npDTs), np.log(npGHTs), color=(1,0,0))
mlab.mesh(np.log(npDs), np.log(npDTs), np.log(npGHPs), color=(0,1,0))
mlab.mesh(np.log(npDs), np.log(npDTs), np.log(npLHTs), color=(0,0,1))

mlab.axes()
mlab.xlabel('Distance', object=None)
mlab.ylabel('Daily Demand', object=None)
mlab.zlabel('Cost per kg of H2', object=None)
#////////////////////////////////////


#pip install mayavi   //>pip install PyQt5
# mlab.surf(npDs, npDTs, npGHTs/10000000, warp_scale="auto", color=(1,0,0))
# mlab.surf(npDs, npDTs, npGHPs/10000000, warp_scale="auto", color=(0,1,0))
# mlab.surf(npDs, npDTs, npLHTs/10000000, warp_scale="auto", color=(0,0,1))

# mlab.axes()
# mlab.xlabel('Distance', object=None)
# mlab.ylabel('Daily Demand', object=None)
# mlab.zlabel('Cost', object=None)
