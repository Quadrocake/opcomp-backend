from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api, abort
from flask_cors import CORS
from flask_socketio import SocketIO
import json
import db
import requests

app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

@socketio.on('connect')
def test_connect():
    print("connected")

import sockets

op_list = {}

def does_not_exist(list_id):
    if list_id not in op_list:
        abort(404, message="List does not exist")

class Comp(Resource):
    def get(self, list_id):
        sql = db.db()
        # does_not_exist(list_id)
        response = json.loads(sql.select_list(list_id))
        print(response)
        return response

    def put(self, list_id):
        sql = db.db()
        print(list_id, json.dumps(request.json), "- put print")
        sql.insert(list_id, json.dumps(request.json))
        # sql.insert("test", "test")
        # op_list[list_id] = request.json
        socketio.emit('db update')
        return 200

    def delete(self, list_id):
        sql = db.db()
        sql.delete(list_id)
        socketio.emit('db update')
        return '', 204

class CompList(Resource):
    def get(self):
        sql = db.db()
        sql.create_table()
        response = {"data": sql.select_complist()}
        # response = {"data": list(op_list.keys())}
        return response

class MALProxy(Resource):
    def get(self):
        url = request.args.get('url')
        if 'myanimelist' in url:
            malReply = requests.get(url, headers={"X-MAL-Client-ID": "6114d00ca681b7701d1e15fe11a4987e"})
            return malReply.json()

api.add_resource(CompList, '/api')
api.add_resource(Comp, '/api/<string:list_id>')
api.add_resource(MALProxy, '/cors')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
