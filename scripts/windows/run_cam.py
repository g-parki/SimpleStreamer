from scripts import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio: SocketIO = SocketIO(app)

if (__name__ == 'main'):
    socketio.run(host='0.0.0.0', port=5750, debug=False)

from . import cam_socket_server