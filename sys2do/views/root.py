# -*- coding: utf-8 -*-
from flask import g, render_template, flash, session, redirect, url_for, request

from sys2do import app
from sys2do.model import connection

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
        session['user_profile'] = {'name' : str(u)}
        return redirect("/index")

def logout_handler():
    session.pop('login', None)
    return redirect("/login")
