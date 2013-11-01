__author__ = 'mcherkassky'

from functools import wraps
from flask import request, Response, g, session, redirect, url_for
from models import User


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'dity' and password == 'awesomeness'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()

        return f(*args, **kwargs)
    return decorated


def load_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except:
        return None


def login_required(f):
    """Decorator that requires admin to login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user_id = session['user_id']
            print user_id
            user = load_user(user_id)
            if user:
                return f(*args, **kwargs)
            else:
                return redirect(url_for('home'))
        except:
            return redirect(url_for('home'))
    return decorated_function

