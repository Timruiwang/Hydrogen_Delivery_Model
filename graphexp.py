# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 15:30:53 2023

@author: Ruiyang Wang
"""
import matplotlib.pyplot as plt
import numpy as np

# data from https://allisonhorst.github.io/palmerpenguins/
#////
# species = (
#     "Adelie\n $\\mu=$3700.66g",
#     "Chinstrap\n $\\mu=$3733.09g",
#     "Gentoo\n $\\mu=5076.02g$",
# )
# weight_counts = {
#     "Below": np.array([70, 31, 58]),
#     "Above": np.array([82, 37, 66]),
# }
# width = 0.5

# fig, ax = plt.subplots()
# bottom = np.zeros(3)

# for boolean, weight_count in weight_counts.items():
#     p = ax.bar(species, weight_count, width, label=boolean, bottom=bottom)
#     bottom += weight_count

# ax.set_title("Number of penguins with above average body mass")
# ax.legend(loc="upper right")

# plt.show()
#///////////
import geopy
from geopy import distance
newport_ri = (41.49008, -71.312796)
cleveland_oh = (41.499498, -81.695391)
print(distance.distance(newport_ri, cleveland_oh).km)

# from fastkml import  kml
# with open('Airports.kml', 'rt', encoding="utf-8") as myfile:
#     doc=myfile.read()
# k = kml.KML()
# k.from_string(doc)
# features = list(k.features())

import pandas as pd
df = pd.read_excel('20230620_UK_Airports_Updated.xlsx')

airports = {}
demands = {}

for i, airport in df.iterrows():
    # name = airport["Airport Name"]
    airports[airport["Airport ID"]] = {
        "Location": (airport["Latitude"], airport["Longitude"]),
        
        "Demand": airport["LH2 to Replace 25% of Kerosene Mass:"],
    }

print(airports)

print(airports[60])

print(distance.distance(airports[60]["Location"], airports[999]["Location"]).km)



import googlemaps
gmap = googlemaps.Client(key='AIzaSyAmspXzRC7nII1T-J5jR4o0mu9phyjEubI')
gmap_output = gmap.distance_matrix(airports[60]["Location"], airports[999]["Location"], mode='driving')
print(gmap_output['rows'][0]['elements'][0]['duration']['value'], 'seconds')
print(gmap_output['rows'][0]['elements'][0]['distance']['value'], 'meters')
#pip install ployly, googlemap
import plotly
import plotly.express as px
from urllib.request import urlopen
mapbox_access_token = "pk.eyJ1IjoidG1yeSIsImEiOiJjbGtiYWY1bHIwZzFjM2Ntc3ltMmQxdXJsIn0.9deNWCvCL6ltXxmbX-Lm3g"



import folium
# from geopy.distance import geodesic
# pizza_map = folium.Map(location=(51.500841300000005, -0.14298782562962786), zoom_start=10)
# # for index,row in df.iterrows(): 
# #   folium.Marker(location=(row['latitude'], 
# #                           row['longitude']), 
# #                 popup=row['postcode']).add_to(pizza_map)

# folium.display(pizza_map)

import pandas as pd
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

# import plotly.express as px

# fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
#                         color_discrete_sequence=["fuchsia"], zoom=3, height=300)
# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()

import pandas as pd
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

import plotly.express as px
import plotly.io as io
# import plotly.graph_objects as go
io.renderers.default='browser'

df["Color"] = np.log(df["LH2 to Replace 25% of Kerosene Mass:"]) - 5

fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_name="Airport Name", size="Color", color="Color", hover_data=["Airport ID", "IATA Code", "ICAO Code", "LH2 to Replace 25% of Kerosene Mass:"],
                        color_discrete_sequence=["fuchsia"], zoom=5, height=1000)
fig.add_trace(px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"]))
# fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
#                         color_discrete_sequence=["fuchsia"], zoom=3, height=300)


# fig.update_layout(
#     mapbox_style="white-bg",
#     mapbox_layers=[
#         {
#             "below": 'traces',
#             "sourcetype": "raster",
#             "sourceattribution": "United States Geological Survey",
#             "source": [
#                 "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
#             ]
#         }
#       ])
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
# for placemark in features[0].features():
#     airports[placemark.name] = (placemark.geometry.x, placemark.geometry.y)
#     print(placemark.name)
#     print(placemark.geometry.x)
#     print(placemark.geometry.y)

# print(airports)
# print(airports["Scatsta Airport"])




# print(list())

# doc = file("Airports.kml").read()
# k = kml.KML()
# k.from_string(doc)
# len(k.features())

g = geopy.geocoders.GoogleV3(api_key="AIzaSyAmspXzRC7nII1T-J5jR4o0mu9phyjEubI")
print(g.geocode("Stansted Airport").latitude)
PLS = "Cambridge"
ID = 1002
tp = (g.geocode(PLS).latitude,g.geocode(PLS).longitude)
print(distance.distance(airports[ID]["Location"],tp))