from functools import wraps
from flask import session, redirect, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Please, login to access this page.", "danger")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function