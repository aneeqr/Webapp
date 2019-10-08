from collections import defaultdict
import numpy as np

def building_inf(gdf_proj):
    v=[]
    cols = list(gdf_proj.columns)
    civilans=['house','residential','terrace','detached','bungalow','dormitory']
    religious=['cathedral','chapel','church','mosque','religious','shrine','synagogue','temple']
    if 'building' in cols:
        d = defaultdict(int,gdf_proj.building.value_counts())
        v.append(gdf_proj['building'].dropna().value_counts().sum()) #Total Buildings
        v.append(len(list(gdf_proj['building'].dropna().unique())))  # Unique Building Types
        v.append(gdf_proj.area.sum()) #total area of buildings
        v.append(gdf_proj.area.mean())#average square metres of buildings
        if 'industrial' in d:
            v.append(d['industrial']) #Total industrial Building count
            v.append( gdf_proj[gdf_proj['building']=='industrial'].area.sum()) 
            v.append( gdf_proj[gdf_proj['building']=='industrial'].area.mean())
            v.append( gdf_proj[gdf_proj['building']=='industrial'].area.median())
            v.append( gdf_proj[gdf_proj['building']=='industrial'].area.max())
        else:
            v.append(np.nan)
            v.append(np.nan)
            v.append(np.nan)
            v.append(np.nan)
            v.append(np.nan)
        my_list=[i for i in civilans if i in list(d.keys())]
        if len(my_list) > 0: #%count and percentage of civilan buildings + area
            area_residental=d['house']+d['residential']+d['terrace']+d['detached']+d['bungalow']+d['dormitory']
            v.append(area_residental)
            v.append(round(area_residental/(gdf_proj['building'].dropna().value_counts().sum()),4))
            area_residental=0
            for i in my_list:
                area_residental+=gdf_proj[gdf_proj['building']==i].area.sum()
            v.append(area_residental)
        else:
            v.append(np.nan)
            v.append(np.nan)
            v.append(np.nan)
        my_list=[i for i in religious if i in list(d.keys())]
        if len(my_list) > 0: #% count religious buildings + area
            area_residental=d['cathedral']+d['chapel']+d['church']+d['mosque']+d['religious']+d['shrine']+d['synagogue']+d['temple']
            v.append(area_residental)
            area_residental=0
            for i in my_list:
                area_residental+=gdf_proj[gdf_proj['building']==i].area.sum()
            v.append(area_residental)
        else:
            v.append(np.nan)
            v.append(np.nan)
        if 'commercial' in d:
            v.append(d['commercial']) #Total commercial buildings count
            v.append(gdf_proj[gdf_proj['building']=='commercial'].area.sum()) #commerical building area
        else:
            v.append(np.nan)
            v.append(np.nan)
        if 'retail' in d:
            v.append(d['retail']) #Total retail buildings count
            v.append(gdf_proj[gdf_proj['building']=='retail'].area.sum()) #retail building area
        else:
            v.append(np.nan)
            v.append(np.nan)
        if 'school' in d:
            v.append(d['school']) #Total school buildings count
            v.append(gdf_proj[gdf_proj['building']=='school'].area.sum()) #school building area
        else:
            v.append(np.nan)
            v.append(np.nan)
        if 'university' in d:
            v.append(d['university']) #Total university count
            v.append(gdf_proj[gdf_proj['building']=='university'].area.sum()) # university area
        else:
            v.append(np.nan)
            v.append(np.nan)
        if 'yes' in d:
            v.append(d['yes']) #Total unclassified count
            v.append(gdf_proj[gdf_proj['building']=='yes'].area.sum()) # unclassified area
        else:
            v.append(np.nan)
            v.append(np.nan)
    else:
        v.append([np.nan]*24)####################13
        v= [item for sublist in v for item in sublist]
        
    if 'amenity' in cols:
        v.append(gdf_proj['amenity'].dropna().value_counts().sum()) # Total amenities
        v.append(len(gdf_proj['amenity'].dropna().unique())) #Tyes of amenities 
    else:
        v.append(np.nan)
        v.append(np.nan)

    if 'tourism' in cols:
        d = defaultdict(int,gdf_proj.tourism.value_counts())
        v.append(len(list(gdf_proj['tourism'].dropna().unique()))) # Types of Tourism
        v.append(gdf_proj.tourism.value_counts().sum()) # Total tourism related stuff
        v.append(d['attraction']) # tourist attractions
    else:
        v.append(np.nan)
        v.append(np.nan)
        v.append(np.nan)

    if 'leisure' in cols:
        v.append(gdf_proj.leisure.value_counts().sum()) # Total Leisure
    else:
        v.append(np.nan)

    return v    
