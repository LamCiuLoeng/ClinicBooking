# -*- coding: utf-8 -*-
import os

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "upload")
UPLOAD_FOLDER_URL = "/static/upload"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc'])
