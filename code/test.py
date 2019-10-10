from flask import Flask,jsonify
from flask_restful import Api, Resource, reqparse
from parsing import parse_init,check_parse
from reverse_geocoding import get_coordinates
from streetlevel import street_level_stats,no_graph_made
from osm_graph import create_graph
from building import building_info
from routing import amenity_by_distance

app = Flask(__name__)
api = Api(app)

# Define parser and request args
parser = parse_init()
# http://127.0.0.1:5000/inf?add1=1 Nethercott Place&add2= Heavitree&town=Exeter&county=Devon&PS=EX1 2TT&network_type=drive&search_radius=1609

class My_Data(Resource):
   def get(self):
       d = check_parse(parser)
       print(d)
       coord = get_coordinates(d.copy())
       v = create_graph(d.copy(),coord)
       if len(v) > 1:
           v = street_level_stats(v)
       else:
           v = no_graph_made()
       v2 = building_info(d.copy(),coord)
       df = v.join(v2)
       #return(df.to_json(orient='records',lines=False)[1:-1].replace('\n',''))#replace('},{', '} {',).replace('{\ ',''))
       return jsonify(df.to_dict('records'))

class Amenities(Resource):
   def get(self):
      d = check_parse(parser)
      coord = get_coordinates(d.copy())
      v = create_graph(d.copy(),coord)
      #print(v)
      if len(v) > 1:
         return(jsonify(amenity_by_distance(v[3],v[0],coord['latitude'],coord['longitude'])))
      else:
         return 'Routing failed, try different search radius'
      

api.add_resource(My_Data, '/inf')
api.add_resource(Amenities,'/route')


if __name__ == '__main__':
    app.run(debug=True,threaded=True)
    #app.config['SERVER_NAME'] = '130.12.12.13'
    #app.run('0.0.0.0',port=5000,debug=False) #host='0.0.0.0'
