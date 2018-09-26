import os
from flask import Flask
from flask_cors import CORS

APP = Flask(__name__)
CORS(APP)
APP.config.from_object('graph_curation_flask.default_settings')
APP.config.from_envvar('GRAPH_CURATION_SETTINGS')

__FORMAT = '[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s'

if not APP.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler
    # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
    file_handler = TimedRotatingFileHandler(
        os.path.join(APP.config['LOG_DIR'],
        'graph_curation.log'), 'midnight'
    )
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(__FORMAT))
    APP.logger.addHandler(file_handler)
