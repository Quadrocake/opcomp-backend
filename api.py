from flask import Flask, request
from flask_restful import Resource, Api, abort
from flask_cors import CORS
import json

app = Flask(__name__)
api = Api(app)
CORS(app)

op_list = {}

def does_not_exist(list_id):
    if list_id not in op_list:
        abort(404, message="List does not exist")

class Comp(Resource):
    def get(self, list_id):
        does_not_exist(list_id)
        response = op_list[list_id]
        return response 

    def put(self, list_id):
        op_list[list_id] = request.json
        response = {list_id: op_list[list_id]}
        return response

    def delete(self, list_id):
        does_not_exist(list_id)
        del op_list[list_id]
        return '', 204

class CompList(Resource):
    def get(self):
        response = {"data": list(op_list.keys())}
        return response

api.add_resource(CompList, '/api')
api.add_resource(Comp, '/api/<string:list_id>')

if __name__ == '__main__':
    app.run()
