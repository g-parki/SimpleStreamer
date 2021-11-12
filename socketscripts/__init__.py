from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio_app: SocketIO = SocketIO(app)