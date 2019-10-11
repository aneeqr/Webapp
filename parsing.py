from flask_restful import Api, Resource, reqparse

def parse_init():
    parser = reqparse.RequestParser()
    parser.add_argument('add1', type=str)   
    parser.add_argument('add2', type=str)
    parser.add_argument('town', type=str)
    parser.add_argument('county', type=str)
    parser.add_argument('country', type=str)
    parser.add_argument('PS',type=str)
    parser.add_argument('network_type',type=str,required=False,help='Please specificy network type, options include: drive, bike, walk',default='drive')
    parser.add_argument('search_radius',type=int,required=False,help='Please specify search radius in metres',default=1609)
    return parser

def check_parse(parser):
    args = parser.parse_args()
    d={'add1':args['add1'],'add2':args['add2'],'town':args['town'],'county':args['county'],'country':args['country'],'PS':args['PS'],'network_type':args['network_type'],'search_radius':args['search_radius']}
    return d


