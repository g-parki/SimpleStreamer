from flask import render_template, Response, stream_with_context
from scripts.app import app, logger
from scripts.streamer import Streamer

@app.route('/watch')
def watch():
    return render_template('watch.html')

@app.route('/feed')
def feed():
    if app.with_socket_client:
        import socketio
        from threading import Event
        from queue import Queue

        client = socketio.Client()
        queue = Queue()
        available_event = Event()
        stop_event = Event()

        def receiver():
            while not stop_event.is_set():
                if not queue.empty():
                    print("yielding something")
                    yield queue.get()
            stop_event.clear()

        @client.on("connect")
        def connect():
            print("connected")

        @client.on("disconnect")
        def disconnect():
            print("disconnected")

        @client.on("frame")
        def frame(data):
            queue.put(data)
            available_event.set()

        client.connect('http://192.168.1.26:5750')
        generator = receiver
        print("Using receiver")
    else:
        stream = Streamer(0)
        generator = stream.http_generate
        print("Using normal streamer")
    return Response(stream_with_context(generator()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/log')
def log():
    with open(logger.LOG_PATH, 'rt+') as f:
        lines = f.readlines()
        # Personally don't care to see calls to log in the log itself...
        lines = [line for line in lines if "log" not in line]
        
    return render_template('log.html', lines= lines or ["No logs"])

@app.route('/clear', methods=["POST"])
def clear():
    with open(logger.LOG_PATH, 'rt+') as f:
        f.truncate(0)
    return "cleared"

@app.after_request
def request_processor(response):
    @response.call_on_close
    def after_request():
        if str(response) == "<Response streamed [200 OK]>":
            logger.log(f"{'- '*8}{logger.timestamp()} Stream closed")
    return response
