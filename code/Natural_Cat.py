import pickle
from fuzzywuzzy import fuzz
import re
from geopy.geocoders import Nominatim
import numpy as np
import operator


def hashvine(lat1,lon1,lat2,lon2):
# approximate radius of earth in km
    R = 6373.0
    from math import sin, cos, sqrt, atan2, radians

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def Nat_Cat(d):
    temp={}
    junkers = re.compile('[{" \}]')
    geolocator = Nominatim(user_agent="my-application")
    d.pop('search_radius')
    d.pop('network_type')
    d = {k:v for k,v in d.items() if v is not None}
    address = geolocator.geocode(' '.join(list(d.values())))
    df = pickle.load(open('NatCatComplete.pkl','rb')).reset_index()
    try:
        for ind,lat,lon in zip(df.index,df.Latitude,df.Longitude): 
            temp[ind]=hashvine(float(address.raw['lat']),float(address.raw['lon']),lat,lon)
        temp2=df[df.index==min(temp.items(), key=operator.itemgetter(1))[0]]
        return dict(zip(junkers.sub('', temp2.NatCat_Names.iloc[0]).split(','),junkers.sub('', temp2.NatCat_Description.iloc[0]).split(',')))
    except:
        address = ' '.join(list(d.values()))
        df = df.drop(15703)
        df = df.reset_index().drop('index',axis=1)
        for ind,add in zip(df.index,df.Address):
            Token_Set_Ratio = fuzz.token_set_ratio(address,add)    
            temp[ind]= Token_Set_Ratio
        temp2=df[df.index==max(temp.items(), key=operator.itemgetter(1))[0]]
        return dict(zip(junkers.sub('', temp2.NatCat_Names.iloc[0]).split(','),junkers.sub('', temp2.NatCat_Description.iloc[0]).split(',')))
         
        

    
    
