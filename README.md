# Webapp

## Getting Building and Street Level Info:
http://127.0.0.1:5000/inf?add1=1 Nethercott Place&add2= Heavitree&town=Exeter&county=Devon&PS=EX1 2TT

## Getting Amenties by distance:
http://127.0.0.1:5000/inf?add1=1 Nethercott Place&add2= Heavitree&town=Exeter&county=Devon&PS=EX1 2TT&network_type=all_private&search_radius=1609

(By default network type is set to drive and search radius is 1609 m)


You can also specify several different network types:

1. drive - get drivable public streets (but not service roads)
2. drive_service - get drivable streets, including service roads
3. walk - get all streets and paths that pedestrians can use (this network type ignores one-way directionality)
4. bike - get all streets and paths that cyclists can use
5. all - download all non-private OSM streets and paths
6. all_private - download all OSM streets and paths, including private-access ones

