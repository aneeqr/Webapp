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
        graph_proj = ox.project_graph(ox.graph_from_point([coord['latitude'],coord['longitude']],distance=1609,network_type='drive'))
        edges_proj = ox.graph_to_gdfs(graph_proj, nodes=False, edges=True)
        v.append(graph_proj)
        v.append(edges_proj)
    except: 
        try: #try address
            graph_proj = ox.project_graph(ox.graph_from_address(' '.join(list(d.values())),distance=1609,network_type='drive'))
            edges_proj = ox.graph_to_gdfs(graph_proj, nodes=False, edges=True)
            v.append(graph_proj)
            v.append(edges_proj)
        except:
            v.append('Graph Not Made!')
    return v
