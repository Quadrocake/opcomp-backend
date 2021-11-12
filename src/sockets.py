from flask import Flask
from flask_socketio import SocketIO
from main import socketio

@socketio.on('connect')
def test_connect():
    print("connected")

@socketio.on('hello server')
def hello():
    socketio.emit('hello client', {'data': 727})