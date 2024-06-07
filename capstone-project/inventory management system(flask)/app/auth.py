from functools import wraps
import logging
from flask import session, render_template

logger = logging.getLogger(__name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'is_admin' not in session or not session['is_admin']:
            logger.warning(f"Unauthorized access attempt for admin by {session.get('username')}")
            return render_template('login.html',message="LogIn as admin to access admin functions")
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or not session['username']:
            logger.warning(f"Unauthorized access attempt for user by {session.get('username')}")
            return render_template('login.html',message="LogIn as admin to access admin functions")
        return f(*args, **kwargs)
    return decorated_function