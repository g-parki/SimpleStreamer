from flask_socketio import SocketIO
from socketscripts import socketio_app
from scripts.streamer import Streamer
from threading import Thread, Event
from threading import enumerate as threadingenumerate
import time

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

counter = ClientCounter()
stop_event = Event()

def emitter(socket: SocketIO, stop_event: Event):
    print("starting emitter")
    stream = Streamer(0)
    while not stop_event.is_set():
        socket.emit("frame", stream.next_frame())
        time.sleep(0.06)
    stop_event.clear()
    print("emitter thread closing")

t = Thread(target=emitter, name="emitter", args=(socketio_app, stop_event), daemon=True)
t.start()

def request_thread():
    threads = [thread.name for thread in threadingenumerate()]
    if "emitter" not in threads:
        #t.start()
        print("Thread is closed. Gotta fix this?")
    else:
        print("Thread already started")

def stop_thread():
    if t.is_alive():
        stop_event.set()
    else:
        print("Thread is already dead")

@socketio_app.on("connect")
def on_connect():
    print("connected")
    counter.increment()
    if counter.count == 1:
        request_thread()
    print(f"Connections: {counter.count}")

@socketio_app.on("disconnect")
def on_disconnect():
    print("disconnected")
    counter.decrement()
    print(f"Connections: {counter.count}")
    if not counter.count:
        stop_thread()
