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
import numpy as np
#%run libraries.py


def amenity_select(element):
    amenities = ['fire_station','police','fuel','pub','hospital','place_of_worship','post_office','pharmacy']
    #amenities=['pub']
    if element in amenities:
        return element    
    return False

def amenity_by_distance(gdf_proj,graph_proj,lat,lon):
    tp={}
    orig_point = Point(utm.from_latlon(lat,lon)[0:2])
    zone_num=utm.from_latlon(lat,lon)[2]
    letter=utm.from_latlon(lat,lon)[3]
    amenities = ['fire_station','police','fuel','pub','hospital','place_of_worship','post_office','pharmacy']
    #amenities=['pub']
    x = pd.DataFrame(gdf_proj['amenity'].dropna().value_counts()).reset_index()
    x = x[x['index'].isin(list(filter(amenity_select,list(gdf_proj['amenity'].dropna().unique()))))]
    x1 = list(x[x['amenity']==1]['index'].values)
    nodes_proj,edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=True)  
    d={}
    d2={}
    orig_node = ox.get_nearest_node(graph_proj, (orig_point.y, orig_point.x), method='euclidean')
    o_closest = nodes_proj.loc[orig_node]
    for i in list(x['index'].dropna().unique()):
        if i in x1:
            target_point = box(*gdf_proj[gdf_proj['amenity']==i].geometry.unary_union.bounds).centroid
            target_node = ox.get_nearest_node(graph_proj, (target_point.y, target_point.x), method='euclidean')
            t_closest = nodes_proj.loc[target_node]
            od_nodes = gpd.GeoDataFrame([o_closest, t_closest], geometry='geometry', crs=nodes_proj.crs)
            route = nx.shortest_path(G=graph_proj, source=orig_node, target=target_node, weight='length')
            route_nodes = nodes_proj.loc[route]
            route_geom = gpd.GeoDataFrame(crs=edges_proj.crs)
            route_geom['geometry'] = None
            route_geom['osmids'] = None
            try:
                route_geom.loc[0, 'geometry'] =  LineString(list(route_nodes.geometry.values))  
                route_geom.loc[0, 'osmids'] = str(list(route_nodes['osmid'].values))
                route_geom['length_m'] = route_geom.length
                target_point=utm.to_latlon(target_point.x,target_point.y,zone_num,letter)
                tp[route_geom['length_m'].values[0]]=target_point
                d2[i]=tp
                
            except:
                route_geom.loc[0, 'geometry'] =  None
                route_geom['length_m'] = 0
                tp[-1]='Not Found'
                d2[i]=tp
            
        else:
            pois = gdf_proj[gdf_proj['amenity']==i]
            dist=[]
            tp_temp={}
            for ind in list(pois.index):
                target_point = box(*pois[pois.index == ind].geometry.unary_union.bounds).centroid
                target_node = ox.get_nearest_node(graph_proj, (target_point.y, target_point.x), method='euclidean')
                t_closest = nodes_proj.loc[target_node]
                od_nodes = gpd.GeoDataFrame([o_closest, t_closest], geometry='geometry', crs=nodes_proj.crs)
                try:
                    route = nx.shortest_path(G=graph_proj, source=orig_node, target=target_node, weight='length')
                    route_nodes = nodes_proj.loc[route]
                    route_geom = gpd.GeoDataFrame(crs=edges_proj.crs)
                    route_geom['geometry'] = None
                    route_geom['osmids'] = None
                    try:
                        route_geom.loc[0, 'geometry'] = LineString(list(route_nodes.geometry.values)) 
                        route_geom.loc[0, 'osmids'] = str(list(route_nodes['osmid'].values))
                        route_geom['length_m'] = route_geom.length
                        target_point=utm.to_latlon(target_point.x,target_point.y,zone_num,letter)
                        tp_temp[route_geom['length_m'].values[0]]=target_point
                    except:
                        route_geom.loc[0, 'geometry'] =  None
                        route_geom['length_m'] = 0
                        #tp_temp[route_geom['length_m'].values[0]]=target_point
                except:
                    route_geom = gpd.GeoDataFrame(crs=edges_proj.crs)
                    route_geom.loc[0, 'geometry'] =  None
                    route_geom['length_m'] = 0            
                dist.append(route_geom['length_m'].values[0])
                
            try:
                tp[min(tp_temp.items(), key=lambda x: x[0])[0]]=tp_temp[min(tp_temp.items(), key=lambda x: x[0])[0]] #distance:point
                d2[i]=tp
            except:
                tp[-1]='Not Found'
                d2[i]=tp
            d[i] = min(dist)
        tp={}
    for key in amenities:
        if key not in d2:
            d2[key]=np.nan    
    return d2
