from collections import defaultdict
import pandas as pd
import pickle
from geopy.geocoders import Nominatim
import re
import pandas as pd
import geopandas as gpd
import osmnx as ox
from shapely.geometry import Point , Polygon, LineString
from pandas.io.json import json_normalize
import utm
import networkx as nx
from shapely.geometry import box
from collections import OrderedDict
import folium
import operator
from routing import amenity_by_distance


def generate_amenities(data,key,graph_map):
    if key == 'pub':
        folium.Marker(location=(list(data[key].values())[0][0],list(data[key].values())[0][1]),icon=folium.Icon(color='darkpurple'),popup='Pub: '+str(round(list(data[key])[0],2))+'m').add_to(graph_map)
    elif key == 'place_of_worship':
        folium.Marker(location=(list(data[key].values())[0][0],list(data[key].values())[0][1]),icon=folium.Icon(color='cadetblue'),popup='POW: '+str(round(list(data[key])[0],2))+'m').add_to(graph_map)
    elif key == 'pharmacy':
        folium.Marker(location=(list(data[key].values())[0][0],list(data[key].values())[0][1]),icon=folium.Icon(color='darkgreen'),popup='Pharmacy: '+str(round(list(data[key])[0],2))+'m').add_to(graph_map)
    elif key == 'fuel':
        folium.Marker(location=(list(data[key].values())[0][0],list(data[key].values())[0][1]),icon=folium.Icon(color='orange'),popup='Fuel: '+str(round(list(data[key])[0],2))+'m').add_to(graph_map)
    elif key == 'hospital':
        folium.Marker(location=(list(data[key].values())[0][0],list(data[key].values())[0][1]),icon=folium.Icon(color='pink'),popup='Hospital: '+str(round(list(data[key])[0],2))+'m').add_to(graph_map)
    elif key == 'fire_station':
        folium.Marker(location=(list(data[key].values())[0][0],list(data[key].values())[0][1]),icon=folium.Icon(color='red'),popup='Fire Station: '+str(round(list(data[key])[0],2))+'m').add_to(graph_map)
    elif key == 'police':
        folium.Marker(location=(list(data[key].values())[0][0],list(data[key].values())[0][1]),icon=folium.Icon(color='gray'),popup='Police: '+str(round(list(data[key])[0],2))+'m').add_to(graph_map)
    elif key == 'post_office':
        folium.Marker(location=(list(data[key].values())[0][0],list(data[key].values())[0][1]),icon=folium.Icon(color='darkblue'),popup='Post Office: '+str(round(list(data[key])[0],2))+'m').add_to(graph_map)
    else:
        pass
    return graph_map

def generate_html(v,coord):
    stats = ox.basic_stats(v[0], area=v[1].unary_union.convex_hull.area)
    for key, value in ox.extended_stats(v[0], ecc=False, bc=True, cc=False,connectivity=False,anc=False).items():
        stats[key] = value
    df1 = pd.DataFrame(list(stats['betweenness_centrality'].values()),list(stats['betweenness_centrality'].keys()),columns=['Value']).reset_index()
    lat=[]
    lon=[]
    for i in list(df1[df1['Value']>0.25]['index'].values):
        lat.append(v[2][v[2].index == i].lat.values[0])
        lon.append(v[2][v[2].index == i].lon.values[0])
    graph_map = ox.plot_graph_folium(v[4], popup_attribute='name', tiles='openstreetmap', edge_width=2)
    folium.Marker(location=(coord['latitude'],coord['longitude']),icon=folium.Icon(color='blue'),popup='Origin').add_to(graph_map)
    if len(lat) > 0:
        for a,b in zip(lat,lon):
            folium.Marker(location=(a,b),icon=folium.Icon(color='beige'),popup='BC:'+str(round(df1[df1['Value']>0.25].Value.values[0],3))).add_to(graph_map)

    data=amenity_by_distance(v[3],v[0],coord['latitude'],coord['longitude'])
    data = {k:v for k,v in data.items() if v != 'Not Found'}
    data = {k:v for k,v in data.items() if pd.Series(v).notna().all()}
    if bool(data) != False:
        graph_map=generate_amenities(data,key,graph_map)
        for key in data:
            graph_map=generate_amenities(data,key,graph_map)
    return graph_map._repr_html_() #iframe  
