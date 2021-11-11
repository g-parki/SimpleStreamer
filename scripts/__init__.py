#Initialize database and app
from flask import Flask
import logging
import os

class MyFlask(Flask):
    def __init__(self, with_socket_client: bool = False):
        super().__init__()
        self.with_socket_client = with_socket_client

app = MyFlask(__name__)

logging.basicConfig(level=logging.INFO)
handler = logging.FileHandler(os.path.join("./scripts", "static", "log.log"), "a")
werk_logger = logging.getLogger('werkzeug')
werk_logger.addHandler(handler)
app.logger.addHandler(handler)

from scripts import routes