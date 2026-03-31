import bcrypt
from flask import Blueprint, render_template, request, flash, redirect, session
from app import db
from app.models import User
import app.validators as valid
from app.decorators import login_required

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template("index.html")

@main.route('/login', methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect("/")

    error = None

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password").encode("utf-8")

        error = valid.validate_login(email, password, User)

        if error:
            flash(error, "danger")
            return redirect("/login")
        
        else:
            user = User.query.filter_by(email=email).one()
            session["user_id"] = user.id

            flash("Logged in!", "success")
            return redirect ("/")
            
    return render_template("login.html")

@main.route('/logout')
def logout():
    session.clear()
    flash("Logged out!", "success")
    
    return redirect(url_for('main.login'))

@main.route('/register', methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect("/")
    
    if request.method == "POST":
        error = None

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        error = valid.validate_register(username, email, password, confirm_password, User)
        
        if error:
            flash(error, "danger")
            return redirect("/register")

        password = password.encode("utf-8")
        hash = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
        
        new_user = User(
            username=username,
            email=email,
            hash=hash,
        )

        try:
            db.session.add(new_user)
            db.session.commit()

            flash("Account Created, login!", "success")
            return redirect("/login")
        
        except Exception:
            db.session.rollback()
            return redirect("/register")

    else:
        return render_template("register.html")