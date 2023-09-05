# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 23:23:43 2023

@author: wry19
"""


import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from cost_functions import calc_costs

D = 60#600
DT = 6000
L = D
  #6000

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

UNIT_Cost_H2_Alkaline = results["UNIT_Cost_H2_Alkaline"]


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

ax.set_title(f"Transportation Cost /kg H2    D{D},DT{DT}")
ax.legend(loc="upper right")
plt.savefig(f'new_costd{D}dt{DT}.png', dpi=1200)

plt.show()

#%%

species = (
    f"LH Truck\n CO2 eq={Emission_LH_TRUCK/f:.2E}kg",
    f"GH Truck\n CO2 eq={Emission_GH_TRUCK/f:.2E}kg",
    f"GH Pipe\n CO2 eq={Emission_GH_PIPE/f:.2E}kg",
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

ax.set_title(f"Transportation Emission /kg H2    D{D},DT{DT}")
ax.legend(loc="upper right")


# plt.savefig(f'emid{D}dt{DT}.png', dpi=1200)
plt.show()

#%%Emission OPEX only
#%%

# species = (
#     f"LH Truck\n CO2={Emission_LH_TRUCK:.2E}\$",
#     f"GH Truck\n cost={Emission_GH_TRUCK:.2E}\$",
#     f"GH Pipe\n cost={Emission_GH_PIPE:.2E}\$",
# )
# weight_counts = {
#     "OPEX_Emission": np.array([Emission_LH_TRUCK_OPEX, Emission_GH_TRUCK_OPEX, Emission_GH_PIPE_OPEX])/f,
# }

# width = 0.5

# fig, ax = plt.subplots()
# bottom = np.zeros(3)
# #////////FROMHERE
# for boolean, weight_count in weight_counts.items():
#     p = ax.bar(species, weight_count, width, label=boolean, bottom=bottom)
#     bottom += weight_count

# ax.set_title("Transportation Emission")
# ax.legend(loc="upper right")

# plt.figure(dpi=2400)
# plt.show()

# print(D,DT)
#print(UNIT_Cost_H2_Alkaline/UNIT_LH_TRUCK , UNIT_Cost_H2_Alkaline/UNIT_GH_TRUCK, UNIT_Cost_H2_Alkaline/UNIT_GH_PIPE)


print(COST_LH_TRUCK_CAPEX/UNIT_LH_TRUCK/f , COST_LH_TRUCK_LAB/UNIT_LH_TRUCK/f, COST_LH_TRUCK_FRE/UNIT_LH_TRUCK/f,COST_LH_TRUCK_ELEC/UNIT_LH_TRUCK/f)
print(COST_GH_TRUCK_CAPEX/UNIT_GH_TRUCK/f , COST_GH_TRUCK_LAB/UNIT_GH_TRUCK/f, COST_GH_TRUCK_FRE/UNIT_GH_TRUCK/f,COST_GH_TRUCK_ELEC/UNIT_GH_TRUCK/f)
print(COST_GH_PIPE_CAPEX/UNIT_GH_PIPE/f , COST_GH_PIPE_OPEX/UNIT_GH_PIPE/f, COST_GH_PIPE_FRE/UNIT_GH_PIPE/f,COST_GH_PIPE_ELEC/UNIT_GH_PIPE/f)


# print(Emission_LH_TRUCK_CAPEX/Emission_LH_TRUCK,Emission_LH_TRUCK_OPEX/Emission_LH_TRUCK)
# print(Emission_GH_TRUCK_CAPEX/Emission_GH_TRUCK,Emission_GH_TRUCK_OPEX/Emission_GH_TRUCK)
# print(Emission_GH_PIPE_CAPEX/Emission_GH_PIPE,Emission_GH_PIPE_OPEX/Emission_GH_PIPE)
# print(0.003 * DT / 1000000000 * 365*5 * 5.8/Emission_GH_TRUCK_OPEX,0.003 * DT / 1000000000 * 365*5 * 5.8/Emission_GH_TRUCK)

# print(0.0944 * L * DT * 365*5 / 1000/Emission_GH_PIPE_OPEX,(0.0944 * L * DT * 365*5 / 1000)/Emission_GH_PIPE)
# print(D)
# from tqdm import tqdm
# for DT in tqdm(range(900, int(1600), int(3))):
#     results = calc_costs(D, DT)
#     COST_LH_TRUCK_CAPEX = results["COST_LH_TRUCK_CAPEX"]
#     COST_GH_TRUCK_CAPEX = results["COST_GH_TRUCK_CAPEX"]
#     COST_GH_PIPE_CAPEX = results["COST_GH_PIPE_CAPEX"]
#     COST_LH_TRUCK_LAB = results["COST_LH_TRUCK_LAB"]
#     COST_GH_TRUCK_LAB = results["COST_GH_TRUCK_LAB"]
#     COST_GH_PIPE_OPEX = results["COST_GH_PIPE_OPEX"]
#     COST_LH_TRUCK_FRE = results["COST_LH_TRUCK_FRE"]
#     COST_GH_TRUCK_FRE = results["COST_GH_TRUCK_FRE"]
#     COST_GH_PIPE_FRE = results["COST_GH_PIPE_FRE"]
#     COST_LH_TRUCK_ELEC = results["COST_LH_TRUCK_ELEC"]
#     COST_GH_TRUCK_ELEC = results["COST_GH_TRUCK_ELEC"]
#     COST_GH_PIPE_ELEC = results["COST_GH_PIPE_ELEC"]
#     UNIT_LH_TRUCK = results["UNIT_LH_TRUCK"]
#     UNIT_GH_TRUCK = results["UNIT_GH_TRUCK"]
#     UNIT_GH_PIPE = results["UNIT_GH_PIPE"]
#     Emission_LH_TRUCK = results["Emission_LH_TRUCK"]
#     Emission_GH_TRUCK = results["Emission_GH_TRUCK"]
#     Emission_GH_PIPE = results["Emission_GH_PIPE"]
#     Emission_LH_TRUCK_OPEX = results["Emission_LH_TRUCK_OPEX"]
#     Emission_GH_TRUCK_OPEX = results["Emission_GH_TRUCK_OPEX"]
#     Emission_GH_PIPE_OPEX = results["Emission_GH_PIPE_OPEX"]
#     Emission_LH_TRUCK_CAPEX = results["Emission_LH_TRUCK_CAPEX"]
#     Emission_GH_TRUCK_CAPEX = results["Emission_GH_TRUCK_CAPEX"]
#     Emission_GH_PIPE_CAPEX = results["Emission_GH_PIPE_CAPEX"]
#     f = results["f"]

#     UNIT_Cost_H2_Alkaline = results["UNIT_Cost_H2_Alkaline"]
#     print(DT,UNIT_LH_TRUCK , UNIT_GH_TRUCK, UNIT_GH_PIPE)
