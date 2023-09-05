# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 15:30:53 2023

@author: wry19
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.io as io
import plotly.graph_objects as go
from urllib.request import urlopen
from random import choice

io.renderers.default = "browser"
mapbox_access_token = "pk.eyJ1IjoidG1yeSIsImEiOiJjbGtiYWY1bHIwZzFjM2Ntc3ltMmQxdXJsIn0.9deNWCvCL6ltXxmbX-Lm3g"

df = pd.read_excel("out2.xlsx")
df["Color"] = np.log(df["LH2 to Replace 25% of Kerosene Mass:"]) - 5

fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Airport Name",
    size="Color",
    color="Color",
    hover_data=[
        "Airport ID",
        "IATA Code",
        "ICAO Code",
        "LH2 to Replace 25% of Kerosene Mass:",
    ],
    color_discrete_sequence=["fuchsia"],
    zoom=5,
    height=1000,
)

colors = [
    "aliceblue",
    "antiquewhite",
    "aqua",
    "aquamarine",
    "azure",
    "beige",
    "bisque",
    "black",
    "blanchedalmond",
    "blue",
    "blueviolet",
    "brown",
    "burlywood",
    "cadetblue",
    "chartreuse",
    "chocolate",
    "coral",
    "cornflowerblue",
    "cornsilk",
    "crimson",
    "cyan",
    "darkblue",
    "darkcyan",
    "darkgoldenrod",
    "darkgray",
    "darkgrey",
    "darkgreen",
    "darkkhaki",
    "darkmagenta",
    "darkolivegreen",
    "darkorange",
    "darkorchid",
    "darkred",
    "darksalmon",
    "darkseagreen",
    "darkslateblue",
    "darkslategray",
    "darkslategrey",
    "darkturquoise",
    "darkviolet",
    "deeppink",
    "deepskyblue",
    "dimgray",
    "dimgrey",
    "dodgerblue",
    "firebrick",
    "floralwhite",
    "forestgreen",
    "fuchsia",
    "gainsboro",
    "ghostwhite",
    "gold",
    "goldenrod",
    "gray",
    "grey",
    "green",
    "greenyellow",
    "honeydew",
    "hotpink",
    "indianred",
    "indigo",
    "ivory",
    "khaki",
    "lavender",
    "lavenderblush",
    "lawngreen",
    "lemonchiffon",
    "lightblue",
    "lightcoral",
    "lightcyan",
    "lightgoldenrodyellow",
    "lightgray",
    "lightgrey",
    "lightgreen",
    "lightpink",
    "lightsalmon",
    "lightseagreen",
    "lightskyblue",
    "lightslategray",
    "lightslategrey",
    "lightsteelblue",
    "lightyellow",
    "lime",
    "limegreen",
    "linen",
    "magenta",
    "maroon",
    "mediumaquamarine",
    "mediumblue",
    "mediumorchid",
    "mediumpurple",
    "mediumseagreen",
    "mediumslateblue",
    "mediumspringgreen",
    "mediumturquoise",
    "mediumvioletred",
    "midnightblue",
    "mintcream",
    "mistyrose",
    "moccasin",
    "navajowhite",
    "navy",
    "oldlace",
    "olive",
    "olivedrab",
    "orange",
    "orangered",
    "orchid",
    "palegoldenrod",
    "palegreen",
    "paleturquoise",
    "palevioletred",
    "papayawhip",
    "peachpuff",
    "peru",
    "pink",
    "plum",
    "powderblue",
    "purple",
    "red",
    "rosybrown",
    "royalblue",
    "rebeccapurple",
    "saddlebrown",
    "salmon",
    "sandybrown",
    "seagreen",
    "seashell",
    "sienna",
    "silver",
    "skyblue",
    "slateblue",
    "slategray",
    "slategrey",
    "snow",
    "springgreen",
    "steelblue",
    "tan",
    "teal",
    "thistle",
    "tomato",
    "turquoise",
    "violet",
    "wheat",
    "white",
    "whitesmoke",
    "yellow",
    "yellowgreen",
]

for name, mini_df in df.groupby("Closest Refuelling Station"):
    color = choice(colors)
    station_lon = mini_df.iloc[0]["Closest Refuelling Station Longitude"]
    station_lat = mini_df.iloc[0]["Closest Refuelling Station Latitude"]


    for i, airport in mini_df.iterrows():
        airport_lon = airport.Longitude
        airport_lat = airport.Latitude


        fig.add_trace(
            go.Scattermapbox(
                mode="lines",
                lon=[airport_lon, station_lon],
                lat=[airport_lat, station_lat],
                line=dict(color=color),
            )
        )

        fig.add_trace(
            go.Scattermapbox(
                mode="markers",
                lon=[airport_lon],
                lat=[airport_lat],
                marker=dict(size=10, symbol=["airport"])
            )
        )
    
    fig.add_trace(
        go.Scattermapbox(
            mode="markers",
            marker=dict(size=10, symbol=["fuel"]),
            lon=[station_lon],
            lat=[station_lat],
        )
    )

# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_layout(
    mapbox_style="open-street-map",
    mapbox = {
        'accesstoken': mapbox_access_token,
        'style': "outdoors", 'zoom': 0.7},
    showlegend = False)

fig.show()
