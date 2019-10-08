import numpy as np
import osmnx as ox
import pandas as pd
import itertools
from collections import defaultdict

def get_mapstatistics(extended_stats):
    v=[]
    keys = list(extended_stats.keys())
#****************************************************************************************************************  
    if 'k_avg' in keys:
        v.append(extended_stats['k_avg'])
    else:
        v.append(np.nan)
#****************************************************************************************************************      
    if 'intersection_count' in keys:
        v.append(extended_stats['intersection_count'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
    if 'streets_per_node_avg' in keys:
        v.append(extended_stats['streets_per_node_avg'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
    if 'edge_length_total' in keys:
        v.append(extended_stats['edge_length_total'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
    if 'edge_length_avg' in keys:
        v.append(extended_stats['edge_length_avg'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
    if 'street_length_total' in keys:
        v.append(extended_stats['street_length_total'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
    if 'street_length_avg' in keys:
        v.append(extended_stats['street_length_avg'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
    if 'street_segments_count' in keys:
        v.append(extended_stats['street_segments_count'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
    if 'node_density_km' in keys:
        if extended_stats['node_density_km'] is not None:
            v.append(extended_stats['node_density_km'])
        else:
            v.append(np.nan)
    else:
        v.append(np.nan)
#****************************************************************************************************************  
    if 'circuity_avg' in keys:
        v.append(extended_stats['circuity_avg'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
    if 'avg_neighbor_degree_avg' in keys:
        v.append(extended_stats['avg_neighbor_degree_avg'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
    if 'avg_weighted_neighbor_degree_avg' in keys:
        v.append(extended_stats['avg_weighted_neighbor_degree_avg'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
    if 'degree_centrality_avg' in keys:
        v.append(extended_stats['degree_centrality_avg'])
    else:
        v.append(np.nan)
#****#************************************************************************************************************  
    if 'clustering_coefficient_avg' in keys:
        v.append(extended_stats['clustering_coefficient_avg'])
    else:
        v.append(extended_stats['clustering_coefficient_avg'])
#****************************************************************************************************************  
    if 'eccentricity' in keys:
        v.append(np.median(np.array(list(extended_stats['eccentricity'].values())))) #median
        v.append(np.mean(np.array(list(extended_stats['eccentricity'].values())))) #mean
    else:
        v.append(np.nan) #median
        v.append(np.nan) #mean
#****************************************************************************************************************  
    if  'closeness_centrality_avg' in keys:
        v.append(extended_stats['closeness_centrality_avg'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
    if 'betweenness_centrality_avg' in keys:
        v.append(extended_stats['betweenness_centrality_avg'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
#****************************************************************************************************************  
    if 'street_density_km' in keys:
        v.append(extended_stats['street_density_km'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  

#****************************************************************************************************************  
    if 'm' in keys:
        v.append(extended_stats['m'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
#****************************************************************************************************************  
    if 'n' in keys:
        v.append(extended_stats['n'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
#****************************************************************************************************************  
    if 'intersection_density_km' in keys:
        v.append(extended_stats['intersection_density_km'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
#****************************************************************************************************************  
    if 'edge_density_km' in keys:
        v.append(extended_stats['edge_density_km'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
#****************************************************************************************************************  
    if 'radius' in keys:
        v.append(extended_stats['radius'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
    if 'diameter' in keys:
        v.append(extended_stats['diameter'])
    else:
        v.append(np.nan)
#****************************************************************************************************************  
    if 'streets_per_node_proportion' in keys:
        temp=defaultdict(int,dict(extended_stats['streets_per_node_proportion']))
        v.append(temp[0])
        v.append(temp[1])
        v.append(temp[2])
        v.append(temp[3])
        v.append(temp[4])
    else:
        v.append(np.nan)
        v.append(np.nan)
        v.append(np.nan)
        v.append(np.nan)
        v.append(np.nan)
#****************************************************************************************************************  
    if 'betweenness_centrality' in keys:
        v.append(max(list(extended_stats['betweenness_centrality'].values())))
        v.append(min(list(extended_stats['betweenness_centrality'].values())))
        v.append(np.median(list(extended_stats['betweenness_centrality'].values())))
    else:
        v.append(np.nan)
        v.append(np.nan)
        v.append(np.nan)
#****************************************************************************************************************  
    return v



def get_edgefeatures(edges_proj):
    v=[]
    cols = list(edges_proj.columns)
    if 'maxspeed' in cols:
        indices=[]
        for ind,value in edges_proj['maxspeed'].items():
            if type(value) == list:
                indices.append(ind)
        try:
            if len(indices) > 0:
                temp = edges_proj['maxspeed'].dropna().copy()
                temp = temp.drop(indices,axis=0) #'' replace('', "", regex=True).
                temp = temp.reset_index().drop('index',axis=1)
                a = pd.isnull(temp.maxspeed)
                indices = list(a[a==True].index)
                temp = temp.drop(indices,axis=0) #'' replace('', "", regex=True). 
                v.append(temp.maxspeed.dropna().str.extract('(\d+)').astype(int).median().values[0])
                v.append(temp.maxspeed.dropna().str.extract('(\d+)').astype(int).max().values[0])
                v.append(temp.maxspeed.dropna().str.extract('(\d+)').astype(int).min().values[0])
                v.append(temp.maxspeed.dropna().str.extract('(\d+)').astype(int).mean().values[0])     
            else:
                v.append(edges_proj['maxspeed'].dropna().str.extract('(\d+)').astype(int).median().values[0])
                v.append(edges_proj['maxspeed'].dropna().str.extract('(\d+)').astype(int).max().values[0])
                v.append(edges_proj['maxspeed'].dropna().str.extract('(\d+)').astype(int).min().values[0])
                v.append(edges_proj['maxspeed'].dropna().str.extract('(\d+)').astype(int).mean().values[0])
        except ValueError:
            temp = edges_proj['maxspeed'].dropna().copy()
            temp = temp.drop(indices,axis=0) #'' replace('', "", regex=True).    
    else:
        v.append(np.nan)
        v.append(np.nan)
        v.append(np.nan)
        v.append(np.nan)
    #******************************************************************************************************    
    # Highways length 
    if 'length' in cols:
        v.append(edges_proj['length'].dropna().median())
        v.append(edges_proj['length'].dropna().max())
        v.append(edges_proj['length'].dropna().min())
        v.append(edges_proj['length'].dropna().mean())
    else:
        v.append(np.nan)
        v.append(np.nan)
        v.append(np.nan)
        v.append(np.nan)
#****************************************************************************************************** 
    if 'highway' in cols:
        indices=[]
        ind=0
        highway_types=0
        highway_lists=[]
        d= edges_proj['highway'].dropna().value_counts()
        d = d.rename_axis('unique_values').reset_index(name='counts') #unique values count
        for key,value in zip(d['unique_values'],d['counts']):
            if type(key) == list:
                highway_lists.append(key)
                highway_types+=len(key)
                indices.append(ind)
            else:
                highway_types+=1
            ind+=1
        if len(indices) > 0:
            d = d.dropna().drop(indices,axis=0)
            d = dict(zip(d['unique_values'], d['counts']))
        else:
            d = dict(zip(d['unique_values'], d['counts']))          
        keys = list(d.keys()) #get keys
        v.append(edges_proj['highway'].dropna().value_counts().sum()) #Total highways
        v.append(highway_types) #Highway Types
        highway_lists=list(itertools.chain.from_iterable(highway_lists))
      #******************************************************************************************************               
        if ('motorway' in keys) or ('motorway' in highway_lists): #presence of motoways
            v.append(1)
        else:
            v.append(0)
      #******************************************************************************************************       
        if ('trunk' in keys) or ('trunk' in highway_lists): #presence of trunks
            v.append(1)
        else:
            v.append(0)
    #******************************************************************************************************     
        if 'primary' in keys or ('primary' in highway_lists): #total primary roads
            v.append(d['primary'])
        else:
            v.append(0)
    #******************************************************************************************************         
        if ('secondary' in keys) or ('secondary' in highway_lists): # total of secondary roads
            v.append(d['secondary'])
        else:
            v.append(0)
    #****************************************************************************************************** 
        if ('residential' in keys) or ('residential' in highway_lists): #residental roads count
            v.append(d['residential'])
        else:
            v.append(0)
    #****************************************************************************************************** 
    else:
        v.append(np.nan) #Total highways
        v.append(np.nan) #Highway Types
        v.append(np.nan) #presence of motoways
        v.append(np.nan) #presence of trunks
        v.append(np.nan) #total primary roads
        v.append(np.nan) # total secondary roads
        v.append(np.nan) #residental roads
#****************************************************************************************************** 
    if 'oneway' in cols:
        d = defaultdict(int,edges_proj.oneway.value_counts(normalize=True)*100)
        
        v.append(round(d[True],4)) #Percentage of highways that are one way       
    else:
        v.append(np.nan) #Total highways
########################################################################################################
    return v      

    



def street_level_stats(v):
    graph_proj=v[0]
    edges_proj= v[1]
    stats = ox.basic_stats(graph_proj, area=edges_proj.unary_union.convex_hull.area)
    extended_stats = ox.extended_stats(graph_proj, ecc=True, bc=True, cc=True)
    for key, value in extended_stats.items():
        stats[key] = value
    extended_stats = dict(pd.Series(stats))
    #keys = list(extended_stats.keys()) 
   # tags = ['k_avg','intersection_count','streets_per_node_avg','edge_length_total',
   ##         'edge_length_avg', 'street_length_total','street_length_avg','street_segments_count',
    #       'node_density_km','circuity_avg','avg_neighbor_degree_avg','avg_weighted_neighbor_degree_avg',
     #      'degree_centrality_avg','clustering_coefficient_avg','eccentricity_median',
      #      'eccentricity_mean','closeness_centrality_avg',
       #    'betweenness_centrality_avg','street_density_km','periphery',
       #     'pagerank_max','pagerank_min','m','n','intersection_density_km',
        #    'edge_density_km']

    # tagsw = ['k_avg','intersection_count','streets_per_node_avg','edge_length_total','edge_length_avg', 'street_length_total','street_length_avg','street_segments_count',
    #       'node_density_km','circuity_avg','street_density_km','m','n','intersection_density_km','edge_density_km']
    values = get_mapstatistics(extended_stats)
    tags=['k_avg','intersection_count','streets_per_node_avg','edge_length_total',
        'edge_length_avg', 'street_length_total','street_length_avg','street_segments_count',
        'node_density_km','circuity_avg','avg_neighbor_degree_avg','avg_weighted_neighbor_degree_avg',
        'degree_centrality_avg','clustering_coefficient_avg','eccentricity_median',
        'eccentricity_mean','closeness_centrality_avg',
        'betweenness_centrality_avg','street_density_km','m','n','intersection_density_km',
        'edge_density_km','radius','diameter','streets_per_node_proportion0',
       'streets_per_node_proportion1','streets_per_node_proportion2','streets_per_node_proportion3',
       'streets_per_node_proportion4','bc_max','bc_min','bc_median']
    tags+=['ms_median',
       'ms_max','ms_min','ms_mean','highwaylen_median','highwaylen_max','highwaylen_min',
       'highwaylen_mean','highway_count','road_types','has_motorways','has_trunks','pr_count','scr_count',
       'resroad_count','percent_oneways']
    values+= get_edgefeatures(edges_proj)
    df = pd.DataFrame([values],columns=tags)
    #out = df.to_json(orient='records')[1:-1].replace('},{', '} {')
    #print(values)
    
    return df#df.to_json(orient='records')[1:-1].replace('},{', '} {')

def no_graph_made():
    tags=['k_avg','intersection_count','streets_per_node_avg','edge_length_total',
        'edge_length_avg', 'street_length_total','street_length_avg','street_segments_count',
        'node_density_km','circuity_avg','avg_neighbor_degree_avg','avg_weighted_neighbor_degree_avg',
        'degree_centrality_avg','clustering_coefficient_avg','eccentricity_median',
        'eccentricity_mean','closeness_centrality_avg',
        'betweenness_centrality_avg','street_density_km','m','n','intersection_density_km',
        'edge_density_km','radius','diameter','streets_per_node_proportion0',
       'streets_per_node_proportion1','streets_per_node_proportion2','streets_per_node_proportion3',
       'streets_per_node_proportion4','bc_max','bc_min','bc_median']
    tags+=['ms_median',
       'ms_max','ms_min','ms_mean','highwaylen_median','highwaylen_max','highwaylen_min',
       'highwaylen_mean','highway_count','road_types','has_motorways','has_trunks','pr_count','scr_count',
       'resroad_count','percent_oneways']
    return (pd.DataFrame([[np.nan]*49],columns=tags))    
