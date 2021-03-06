'''
Created on 2011-4-21

@author: cl.lam
'''
import traceback
from functools import wraps

from flask import g, request, redirect, url_for, render_template, session, flash
from flask import current_app as app

from sys2do.util.common import MESSAGE_ERROR


__all__ = ['login_required', 'templated', 'has_all_permissions', 'is_all_roles', 'is_any_roles']


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        app.logger.info("COME INTO LOGIN")
        if not session.get('login', None):
            return redirect(url_for('login', next = request.url))
        return f(*args, **kwargs)
    return decorated_function


def templated(template = None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator


def has_all_permissions(ps = [], message = "You do not get the permissions !", url = "/index"):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if all(map(lambda p:p in session['user_profile']['permissions'], ps)):
                    return f(*args, **kwargs)
            except:
                app.logger.error(traceback.format_exc())
            flash(message, MESSAGE_ERROR)
            return redirect(url)
        return decorated_function
    return decorator


def has_any_permissions(ps = [], message = "You do not get the permissions !", url = "/index"):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if any(map(lambda p:p in session['user_profile']['permissions'], ps)):
                    return f(*args, **kwargs)
            except:
                app.logger.error(traceback.format_exc())
            flash(message, MESSAGE_ERROR)
            return redirect(url)
        return decorated_function
    return decorator


def is_all_roles(ps = [], message = "You do not get the the permissions !", url = "/index"):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if all(map(lambda p:p in session['user_profile']['roles'], ps)):
                    return f(*args, **kwargs)
            except:
                app.logger.error(traceback.format_exc())
            flash(message, MESSAGE_ERROR)
            return redirect(url)
        return decorated_function
    return decorator



def is_any_roles(ps = [], message = "You do not get the permissions !", url = "/index"):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if any(map(lambda p:p in session['user_profile']['roles'], ps)):
                    return f(*args, **kwargs)
            except:
                app.logger.error(traceback.format_exc())
            flash(message, MESSAGE_ERROR)
            return redirect(url)
        return decorated_function
    return decorator
