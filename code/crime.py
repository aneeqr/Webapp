import pickle
from fuzzywuzzy import fuzz
import re
from geopy.geocoders import Nominatim
import numpy as np
import operator


def Crime(d):
    df=pickle.load(open('Crime.pkl','rb'))
    temp={}
    junkers = re.compile('[{" \}]')
    geolocator = Nominatim(user_agent="my-application")
    d.pop('search_radius')
    d.pop('network_type')
    d = {k:v for k,v in d.items() if v is not None}
    address = geolocator.geocode(' '.join(list(d.values())))
    try:
        for ind,add in zip(df.index,df.Community):
            Token_Set_Ratio = fuzz.token_set_ratio(address.address,add)
            temp[ind]= Token_Set_Ratio
        return(df[df.index==max(temp.items(), key=operator.itemgetter(1))[0]])
    except:
        address = ' '.join(list(d.values()))
        for ind,add in zip(df.index,df.Community):
            Token_Set_Ratio = fuzz.token_set_ratio(address,add)
            temp[ind]= Token_Set_Ratio
        return(df[df.index==max(temp.items(), key=operator.itemgetter(1))[0]])       
