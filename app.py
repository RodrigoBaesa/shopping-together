import bcrypt
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from validators import validate_register
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    hash = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        error = None

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        error = validate_register(username, email, password, confirm_password, User)
        if error:
            flash(error, "danger")

            return redirect("/register")

        password = password.encode("utf-8")
        hash = bcrypt.hashpw(password, bcrypt.gensalt())
        
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)