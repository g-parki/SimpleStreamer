from scripts import app
import socketio
from threading import Event
from queue import Queue

client = socketio.Client()
client.connect('http://localhost:5750')

class Receiver:
    def __init__(self):
        self.queue = Queue()
        self.event = Event()

    def generate(self):
        while True:
            self.event.wait()
            if self.queue.not_empty:
                yield self.queue.get()
            self.event.clear()

receiver = Receiver()

@client.on("frame available")
def receive(data):
    receiver.queue.put(data)
    receiver.event.set()