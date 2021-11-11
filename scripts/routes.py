import os
from datetime import datetime
from flask import render_template, Response, stream_with_context
from scripts import app, werk_logger
from scripts.streamer import Streamer

LOG_PATH = os.path.join(os.getcwd(),'scripts','static', 'log.log')

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
    with open(LOG_PATH, 'r+') as f:
        lines = f.readlines()

        # Personally don't care to see calls to log in the log itself...
        lines = [line for line in lines if "log" not in line]
        f.truncate(0)
        f.writelines(lines)
        
    return render_template('log.html', lines= lines or ["No logs"])

@app.route('/clear', methods=["POST"])
def clear():
    with open(LOG_PATH, 'r+') as f:
        f.truncate(0)
    return "cleared"

@app.after_request
def request_processor(response):
    @response.call_on_close
    def after_request():
        if str(response) == "<Response streamed [200 OK]>":
            date = datetime.now().strftime("[%d/%b/%Y %H:%M:%S]")
            werk_logger.info(f"{'- '*8}{date} Stream closed")
    return response
