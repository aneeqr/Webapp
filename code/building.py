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
    print(d)
    print(d['search_radius'])
    tags = ['total_buildings','construction_types','Totalbuildingarea',
       'Buildingarea_avg','industrialbuildings_count','industrialbuildingsarea_sum',
       'industrialbuildingsarea_mean','industrialbuildingsarea_median','industrialbuildingsarea_max',
       'residential_count','percent_civilarea','residential_area','religiousbuildings_count','religiousbuildings_area',
        'commercial_count','commercial_area','retial_count','retail_area','school_count','school_area',
        'uni_count','uni_area','unclass_count','unclass_area','amenities_type','amenity_total','pub_count','fastfood_count','college_count','library_count','school_count','university_count',
        'fuel_count','hospital_count','pharmacy_count','clinic_count','cinema_nightclubs_count',
        'fire_station_count','place_of_worship_count','policestation_count','prison_count','post_office_count',
        'marketplace_count','bank_count','toursim_type','toursim_total','toursim_attractions','leisure_count']
    try:
        # try graph from point
        #print(d['search_radius'])
        gdf_proj = ox.project_gdf(ox.footprints_from_point(point=[coord['latitude'],coord['longitude']], distance=d['search_radius']))
        v = building_inf(gdf_proj)
        v = pd.DataFrame([v],columns=tags)
    except:
        try: #Go Graph from address
            #print(d['search_radius'])
            gdf_proj = ox.project_gdf(ox.footprints_from_address(' '.join(list(d.values())), distance=d['search_radius']))
            v=building_inf(gdf_proj)
            v = pd.DataFrame([v],columns=tags)
        except:
            v.append([np.nan]*48)
            v=pd.DataFrame(v,columns=tags)    
    return v


