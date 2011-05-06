# -*- coding: utf-8 -*-
'''
Created on 2011-5-5

@author: cl.lam
'''
import datetime
from jinja2.filters import do_default
#from flask import current_app as app
#from sys2do import app

__all__ = ['todayBefor', 'formatTime', 'formatDate', 'ifFalse']


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

def ifFalse(v, default = u""):
    return do_default(v, default) or default
