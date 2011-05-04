# -*- coding: utf-8 -*-

from flask import Flask, Module


__all__ = ["app"]

app = Flask(__name__, static_path = '/static')
app.debug = True


#===============================================================================
# sys.py
#===============================================================================
import views.sys as s
for error_code in [403, 404, 500] : app.error_handlers[error_code] = s.error_page(error_code)


#===============================================================================
# root.py
#===============================================================================
import views.root as r
app.add_url_rule("/", view_func = r.index)
app.add_url_rule("/index", view_func = r.index)
app.add_url_rule("/login", view_func = r.login)
app.add_url_rule("/login_handler", view_func = r.login_handler, methods = ['GET', 'POST'])
app.add_url_rule("/logout_handler", view_func = r.logout_handler, methods = ['GET', 'POST'])

import views.action as a
app.add_url_rule("/list_clinic", view_func = a.list_clinic)
app.add_url_rule("/list_doctor", view_func = a.list_doctor)
app.add_url_rule("/schedule", view_func = a.schedule)
