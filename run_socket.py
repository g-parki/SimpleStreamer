from socketscripts import socketio_app, app
from socketscripts import cam_socket_server

if __name__ == "__main__":
    socketio_app.run(app, host='192.168.1.26', port=5750, debug=True)

    