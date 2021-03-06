# -*- coding: utf-8 -*-
'''
Created on 2011-5-5

@author: cl.lam
'''
import datetime
from jinja2.filters import do_default
#from flask import current_app as app
#from sys2do import app

__all__ = ['todayBefor', 'formatTime', 'formatDate', 'string2Date', 'ifFalse', 'getByID', 'ampm']


def todayBefor(d):
    if type(d) == datetime.datetime : return d < datetime.datetime.today()
    if type(d) == datetime.date : return d <= datetime.datetime.today().date()
    return False



def formatTime(t, f = "%Y-%m-%d %H:%M%S"):
    try:
        return t.strftime(f)
    except:
        return str(t)


def formatDate(d, f = "%Y-%m-%d"):
    try:
        return d.strftime(f)
    except:
        return str(d)


def string2Date(v):
    return "%s-%s-%s" % (v[:4], v[4:6], v[-2:])

def ifFalse(v, default = u""):
    return do_default(v, default) or default


def getByID(id, obj, attr):
    from sys2do.model import connection
    v = getattr(getattr(connection, obj).one({"id" : id}), attr)
    return v() if callable(v) else v


def ampm(v):
    try:
        h, m = v.split(":")
        h = int(h)
        if h < 12 :
            return "%.2d:%s AM" % (h, m)
        if h == 24 :
            return "00:00 AM"
        else:
            return "%.2d:%s PM" % (h - 12, m)
    except:
        return v
