import os
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config["SESSION_PERMANENT"] = False
    app.config['SESSION_TYPE'] = 'filesystem'

    Session(app)
    db.init_app(app)

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app