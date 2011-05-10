# -*- coding: utf-8 -*-
from flask import g, render_template, flash, session, redirect, url_for, request

from sys2do import app
from sys2do.model import connection
from flask.helpers import jsonify

def index():
    if 'login' not in session or not session['login']:
        return redirect(url_for('login'))
    user_profile = session['user_profile']
    app.logger.debug('A value for debugging')
    return render_template("index.html", user_profile = user_profile)


def login():
    if session.get('login', None):
        return redirect("/index")
    return render_template("login.html")


def login_handler():
    email = request.values.get('email', None)
    password = request.values.get('password', None)
    u = connection.User.one({'active' : 0, 'email':email, 'password':password})
    if not u:
        flash("e-mail or password is not correct !")
        return redirect("/login")
    else:
        session['login'] = True
        session['user_profile'] = u.populate()
        return redirect("/index")

def logout_handler():
    session.pop('login', None)
    return redirect("/login")


def search():
    q = request.values.get('q', None)
    r = connection.Role.one({"name":"DOCTOR"})
    contain = {"$regex" : "/.*%s.*/i" % q}
    contain = "/.*%s.*/i" % q
    #search the user
    us = connection.User.find({
                               'active' : 0,
                               'roles':{'$all':[r.id]},
                               '$or':[{'first_name' : contain},
#                                      {'last_name' : contain},
                                 ]
                          })
    data = [u.populate() for u in us]
    app.logger.info(data)
    return jsonify(data)
