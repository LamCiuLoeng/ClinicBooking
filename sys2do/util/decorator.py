'''
Created on 2011-4-21

@author: cl.lam
'''
from functools import wraps
from flask import g, request, redirect, url_for, render_template, session
from flask import current_app as app


__all__ = ['login_required']


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
