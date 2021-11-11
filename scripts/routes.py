from flask import render_template, Response, stream_with_context
from scripts import app, logger
from scripts.streamer import Streamer

@app.route('/watch')
def watch():
    return render_template('watch.html')

@app.route('/feed')
def feed():
    if app.with_socket_client:
        from scripts import socket_client
        generator = socket_client.receiver.generate
    else:
        stream = Streamer()
        generator = stream.http_generate
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
