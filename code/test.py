from flask import Flask,jsonify
from flask_restful import Api, Resource, reqparse
from parsing import parse_init,check_parse
from reverse_geocoding import get_coordinates
from streetlevel import street_level_stats,no_graph_made
from osm_graph import create_graph
from building import building_info

app = Flask(__name__)
api = Api(app)

# Define parser and request args
parser = parse_init()


class My_Data(Resource):
   def get(self):
       d = check_parse(parser)
       coord = get_coordinates(d)
       v = create_graph(d,coord)
       if len(v) > 1:
           v = street_level_stats(v)
       else:
           v = no_graph_made()
       v2 = building_info(d,coord)
       df = v.join(v2)
       #return(df.to_json(orient='records',lines=False)[1:-1].replace('\n',''))#replace('},{', '} {',).replace('{\ ',''))
       return jsonify(df.to_dict('records'))

api.add_resource(My_Data, '/inf')


if __name__ == '__main__':
    app.run(debug=True,threaded=True)
    #app.config['SERVER_NAME'] = '130.12.12.13'
    #app.run('0.0.0.0',port=5000,debug=False) #host='0.0.0.0'
