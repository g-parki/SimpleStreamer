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

class Emitter:
    
    def __init__(self, stream: Streamer, socket: SocketIO):
        self._stream = stream
        self._socket = socket
        self._emitting: bool = False
        self.counter = ClientCounter()

    def emit(self):
        while self.counter.count:
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
        self._emitter.counter.increment()
        self._emitter.request_emit()

    @socketio.on("disconnect")
    def decrease_count(self):
        self._emitter.counter.decrement()