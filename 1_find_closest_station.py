
"""
Created on Tue Aug 15 2023

@author: Ruiyang Wang
"""
import pandas as pd
from geopy.distance import distance

refuelling_stations_df = pd.read_csv("Refuelling_stations.csv")
airports_df = pd.read_excel("20230620_UK_Airports_Updated.xlsx")

# print(refuelling_stations)
# print(airports)

# airports_df["Closest Refuelling Station"]

for i, airport in airports_df.iterrows():
    closest_rs = None
    min_distance = float('inf')
    for j, rs in refuelling_stations_df.iterrows():
        airport_loc = (airport.Latitude, airport.Longitude)
        rs_loc = (rs.Latitude, rs.Longitude)
        d = distance(airport_loc, rs_loc).km
        
        if d < min_distance:
            closest_rs = rs
            min_distance = d
    
    print(i, ": ", airport["Airport Name"], " -- ", closest_rs.Name)

    airports_df.loc[i, "Closest Refuelling Station"] = closest_rs.Name
    airports_df.loc[i, "Closest Refuelling Station Distance"] = min_distance
    airports_df.loc[i, "Closest Refuelling Station Latitude"] = closest_rs.Latitude
    airports_df.loc[i, "Closest Refuelling Station Longitude"] = closest_rs.Longitude

print(airports_df)

airports_df.to_excel("out.xlsx")