from flask_restful import Api, Resource, reqparse

def parse_init():
    parser = reqparse.RequestParser()
    parser.add_argument('add1', type=str)   
    parser.add_argument('add2', type=str)
    parser.add_argument('town', type=str)
    parser.add_argument('county', type=str)
    parser.add_argument('country', type=str)
    parser.add_argument('PC',type=str)
    return parser

def check_parse(parser):
    args = parser.parse_args()
    d={'add1':args['add1'],'add2':args['add2'],'town':args['town'],'county':args['county'],'country':args['country'],'PC':args['PC']}
    return d
    
