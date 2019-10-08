import numpy as np
import geopandas as gpd
import pandas as pd
from pandas.io.json import json_normalize
import osmnx as ox
import networkx as nx
from shapely.geometry import box
from collections import OrderedDict
from building_features import building_inf



def building_info(d,coord):
    v=[]
    tags = ['total_buildings','construction_types','Totalbuildingarea',
       'Buildingarea_avg','industrialbuildings_count','industrialbuildingsarea_sum',
       'industrialbuildingsarea_mean','industrialbuildingsarea_median','industrialbuildingsarea_max',
       'residential_count','percent_civilarea','residential_area','religiousbuildings_count','religiousbuildings_area',
        'commercial_count','commercial_area','retial_count','retail_area','school_count','school_area',
        'uni_count','uni_area','unclass_count','unclass_area','amenities_total','amenities_type','toursim_type','toursim_total','toursim_attractions','leisure_count']
    try:
        # try graph from point
        gdf_proj = ox.project_gdf(ox.footprints_from_point(point=[coord['latitude'],coord['longitude']], distance=1609))
        v = building_inf(gdf_proj)
        v = pd.DataFrame([v],columns=tags)
    except:
        try: #Go Graph from address
            gdf_proj = ox.project_gdf(ox.footprints_from_address(' '.join(list(d.values())), distance=1609))
            v=building_inf(gdf_proj)
            v = pd.DataFrame([v],columns=tags)
        except:
            v.append([np.nan]*20)
            v=pd.DataFrame(v,columns=tags)    
    return v


