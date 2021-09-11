from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def some_function():
    socketio.emit('some event', {'data': 42})

@socketio.on('connect')
def test_connect():
    print("connected")

@socketio.on('hello server')
def hello():
    socketio.emit('hello client', {'data': 727})

if __name__ == '__main__':
    socketio.run(app)