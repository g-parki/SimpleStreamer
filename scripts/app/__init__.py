#Initialize database and app
from flask import Flask
from datetime import datetime
import logging
import os

class MyFlask(Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.with_socket_client = False

app = MyFlask(__name__)

class Logger:

    LOG_PATH = os.path.join(os.getcwd(),'scripts','app', 'static', 'log.log')
    handler = logging.FileHandler(LOG_PATH, "a")
    
    def __init__(self, app: MyFlask):
        logging.basicConfig(level=logging.INFO)
        self._applogger = app.logger
        self._werklogger = logging.getLogger('werkzeug')

        self._applogger.addHandler(Logger.handler)
        self._werklogger.addHandler(Logger.handler)

    def log(self, message: str) -> None:
        self._werklogger.info(message)

    @staticmethod
    def timestamp() -> str:
        return datetime.now().strftime("[%d/%b/%Y %H:%M:%S]")

logger = Logger(app)
logger.log(f'\n {logger.timestamp()} server started')

from . import routes