import socketio
from threading import Event
from queue import Queue

client = socketio.Client()
queue = Queue()
available_event = Event()
stop_event = Event()

def receiver():
    while not stop_event.is_set():
        available_event.wait()
        print("Returning something")
        yield queue.get()
        available_event.clear()
    stop_event.clear()


@client.on("connect")
def connect():
    print("connected")

@client.on("disconnect")
def disconnect():
    print("disconnected")

@client.on("frame")
def frame(data):
    receiver.queue.put(data)
    receiver.event.set()

client.connect('http://192.168.1.26:5750')