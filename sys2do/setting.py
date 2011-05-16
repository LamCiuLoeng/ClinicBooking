# -*- coding: utf-8 -*-
import os, datetime, uuid, logging

DEBUG = True

#upload setting
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "upload")
UPLOAD_FOLDER_URL = "/static/upload"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc'])


#session setting
SECRET_KEY = str(uuid.uuid4())
USE_X_SENDFILE = False
SERVER_NAME = None
MAX_CONTENT_LENGTH = None
TESTING = False
PERMANENT_SESSION_LIFETIME = datetime.timedelta(31)
SESSION_COOKIE_NAME = 'session'


#config for logging
LOGGING_FILE = True
LOGGING_FILE_PATH = os.path.join(os.path.dirname(__file__), "log.txt")
LoGGING_LEVEL = logging.INFO
