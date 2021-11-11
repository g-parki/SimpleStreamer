from flask_socketio import SocketIO
from scripts import socketio
from scripts.streamer import Streamer

class ClientCounter:

    def __init__(self):
        self._count: int = 0
    
    def increment(self):
        self._count += 1

    def decrement(self):
        self._count -= 1
    
    @property
    def count(self):
        return self._count

class Emitter(ClientCounter):
    
    def __init__(self, stream: Streamer, socket: SocketIO):
        self._stream = stream
        self._socket = socket
        self._emitting: bool = False

    def emit(self):
        while self._count:
            self._emitting = True
            try:
                self._socket.emit("frame available", {"frame": self._stream.next_frame()}, broadcast=True)
            except:
                break
        self._emitting = False

    def request_emit(self):
        if not self._emitting:
            self.emit()

class Router:
    
    def __init__(self):
        self._emitter: Emitter = Emitter(Streamer(), socketio)

    @socketio.on("connect")
    def increase_count(self):
        self._emitter.increment()
        self._emitter.request_emit()

    @socketio.on("disconnect")
    def decrease_count(self):
        self._emitter.decrement()