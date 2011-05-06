# -*- coding: utf-8 -*-
'''
Created on 2011-5-6

@author: cl.lam
'''
from flask import g, render_template, flash, session, redirect, url_for, request

__all__ = ['MESSAGE_INFO', 'MESSAGE_ERROR', '_g']

MESSAGE_INFO = "INFO"
MESSAGE_ERROR = "ERROR"


def _g(name, default = None):
    return request.values.get(name, default)
