import geopandas as gpd
import pandas as pd
from pandas.io.json import json_normalize
import osmnx as ox
import networkx as nx
from shapely.geometry import box
from collections import OrderedDict




def create_graph(d,coord):
    v=[]
    try: #try coordinates
        graph_proj = ox.project_graph(ox.graph_from_point([coord['latitude'],coord['longitude']],distance=d['search_radius'],network_type=d['network_type']))
        nodes_proj,edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=True)
        gdf_proj = ox.project_gdf(ox.footprints_from_point(point=[coord['latitude'],coord['longitude']], distance=d['search_radius']))
        v.append(graph_proj)
        v.append(edges_proj)
        v.append(nodes_proj)
        v.append(gdf_proj)
    except: 
        try: #try address
            #temp=d.copy()
            d.pop('search_radius')
            d.pop('network_type')
            d = {k:v for k,v in d.items() if v is not None}
            graph_proj = ox.project_graph(ox.graph_from_address(' '.join(list(d.values())),distance=temp['search_radius'],network_type=temp['network_type']))
            nodes_proj,edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=True)
            gdf_proj = ox.project_gdf(ox.footprints_from_address(' '.join(list(d.values())), distance=temp['search_radius']))

            v.append(graph_proj)
            v.append(edges_proj)
            v.append(nodes_proj)
            v.append(gdf_proj)
        except:
            v.append('Graph Not Made!')
    return v


def create_graph2(d,coord):
    v=[]
    try: #try coordinates
        G = ox.graph_from_point([coord['latitude'],coord['longitude']],distance=d['search_radius'],network_type=d['network_type'])
        graph_proj = ox.project_graph(G)
        nodes_proj,edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=True)
        gdf_proj = ox.project_gdf(ox.footprints_from_point(point=[coord['latitude'],coord['longitude']], distance=d['search_radius']))
        v.append(graph_proj)
        v.append(edges_proj)
        v.append(nodes_proj)
        v.append(gdf_proj)
        v.append(G)
    except: 
        try: #try manual coordinates enter search
            G = ox.graph_from_point([d['Lat'],d['Lon']],distance=d['search_radius'],network_type=d['network_type'])
            graph_proj = ox.project_graph(G)
            nodes_proj,edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=True)
            gdf_proj = ox.project_gdf(ox.footprints_from_point(point=[d['latitude'],d['longitude']], distance=d['search_radius']))

            v.append(graph_proj)
            v.append(edges_proj)
            v.append(nodes_proj)
            v.append(gdf_proj)
            v.append(G)
        except:
            v.append('Graph Not Made!')
    return v
