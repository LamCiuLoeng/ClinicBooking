# -*- coding: utf-8 -*-
'''
Created on 2011-5-6

@author: cl.lam
'''
import os
from datetime import datetime as dt
from flask import g, render_template, flash, session, redirect, url_for, request
from werkzeug import secure_filename
from flask import current_app as app

from sys2do.setting import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, UPLOAD_FOLDER_URL
from sys2do.model import connection, UploadFile

__all__ = ['MESSAGE_INFO', 'MESSAGE_ERROR', '_g', 'upload', 'makeException']

MESSAGE_INFO = "INFO"
MESSAGE_ERROR = "ERROR"


def _g(name, default = None):
    return request.values.get(name, default)

def _gl(name, default = []):
    return request.form.getlist(name, default)


def _allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload(name):
    f = request.files.get(name, None)
    if not f : raise makeException("No file upload!")
    if _allowedFile(f.filename):
        if not os.path.exists(UPLOAD_FOLDER) : os.makedirs(UPLOAD_FOLDER)
        converted_name = "%s.%s" % (dt.now().strftime("%Y%m%d%H%M%S"), f.filename.rsplit('.', 1)[1].lower())
        path = os.path.join(UPLOAD_FOLDER, converted_name)
        f.save(path)
        u = connection.UploadFile()
        u.id = u.getID()
        u.uid = session['user_profile']['id']
        u.name = unicode(secure_filename(f.filename))
        u.path = path
        u.url = "/".join([UPLOAD_FOLDER_URL, converted_name])
        u.save()
        return u
    else:
        raise makeException("Invalid file to upload!")


def makeException(msg):
    class _ExceptionClz(Exception):
        def __init__(self, msg = msg):
            self.msg = msg
            self.is_customize = True

        def __str__(self): return self.msg
        def __unicode__(self): return self.msg
        def __repr__(self): return self.msg

    return _ExceptionClz
