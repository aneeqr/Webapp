from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="my-application")
#http://127.0.0.1:5000/inf?add1=8 Cranmere Court&town=Exeter&county=Devon&PS=EX2 8 PW
#http://127.0.0.1:5000/inf?add1=1 Nethercott Place&add2= Heavitree&town=Exeter&county=Devon&PS=EX1 2TT


def get_coordinates(d):
    d={k:v for k,v in d.items() if v is not None}
    d.pop('search_radius')
    d.pop('network_type')
    #print(d)
    #print(' '.join(list(d.values())))
    location = geolocator.geocode(' '.join(list(d.values())))
    return {'latitude':location.latitude,'longitude':location.longitude}
