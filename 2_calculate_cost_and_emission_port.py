"""
Created on Tue Aug 15 2023

@author: Ruiyang Wang
"""
from cost_functions import calc_costs, get_min_cost
import pandas as pd

airports_df = pd.read_excel("out_port.xlsx")

for i, airport in airports_df.iterrows():
    costs = calc_costs(airport["Closest Port Distance"], airport["LH2 to Replace 25% of Kerosene Mass:"])

    min_name, min_value = get_min_cost(costs, ["UNIT_LH_TRUCK", "UNIT_GH_TRUCK", "UNIT_GH_PIPE"])
    airports_df.loc[i, "Delivery Cost Min"] = min_value
    airports_df.loc[i, "Delivery Method Min By Cost"] = min_name.lstrip("UNIT_")

    emission_name = "UNIT_Emission_" + min_name.lstrip("UNIT_")
    emission_value = costs[emission_name]
    airports_df.loc[i, "Min Cost Emission"] = emission_value


    min_name, min_value = get_min_cost(costs, ["UNIT_Emission_LH_TRUCK", "UNIT_Emission_GH_TRUCK", "UNIT_Emission_GH_PIPE"])
    airports_df.loc[i, "Delivery Emission Min"] = min_value
    airports_df.loc[i, "Delivery Method Min By Emission"] = min_name.lstrip("UNIT_Emission_")

    cost_name = "UNIT_" + min_name.lstrip("UNIT_Emission_")
    cost_value = costs[cost_name]
    airports_df.loc[i, "Min Emission Cost"] = cost_value



print(airports_df)

airports_df.to_excel("out2_port.xlsx")
