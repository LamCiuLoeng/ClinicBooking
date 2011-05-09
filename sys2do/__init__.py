# -*- coding: utf-8 -*-

from flask import Flask, Module


__all__ = ["app"]

app = Flask(__name__, static_path = '/static')
app.debug = True
app.secret_key = 'K\x11\xadt\x1e\xb5k(zJ\xa7}\xa6\xda\xb2.\xecb\x81p\xbbU\xa2\xcf'

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
app.add_url_rule("/list_doctors", view_func = a.list_doctors)
app.add_url_rule("/list_doctors_by_clinic", view_func = a.list_doctors_by_clinic)
app.add_url_rule("/schedule", view_func = a.schedule)
app.add_url_rule("/save_events", view_func = a.save_events, methods = ['GET', 'POST'])
app.add_url_rule("/my_booking", view_func = a.my_booking, methods = ['GET', 'POST'])
app.add_url_rule("/my_message", view_func = a.my_message, methods = ['GET', 'POST'])

import views.manage as m
app.add_url_rule("/m_clinic", view_func = m.m_clinic_list)
app.add_url_rule("/m_clinic_update", view_func = m.m_clinic_update)
app.add_url_rule("/m_clinic_save", view_func = m.m_clinic_save, methods = ['POST'])
app.add_url_rule("/m_doctor", view_func = m.m_doctor_list)
app.add_url_rule("/m_doctor_update", view_func = m.m_doctor_update)
app.add_url_rule("/m_doctor_save", view_func = m.m_doctor_save, methods = ['POST'])
app.add_url_rule("/m_nurse", view_func = m.m_nurse_list)
app.add_url_rule("/m_user", view_func = m.m_user_list)


#===============================================================================
# import the cuxtomize filter
#===============================================================================
import util.filters as filters
for f in filters.__all__ : app.jinja_env.filters[f] = getattr(filters, f)
