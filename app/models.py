from sqlalchemy import null

from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)
    hash = db.Column(db.Text, nullable=False)
    family = db.Column(db.Integer, db.ForeignKey("families.id"), default=None)

class List(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    family_id = db.Column(db.Integer, db.ForeignKey("families.id"))

class Item (db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    brand = db.Column(db.String(100), nullable=False)
    bought = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey("lists.id"))

class Family (db.Model):
    __tablename__ = "families"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Invite(db.Model):
    __tablename__ = 'invites'
    id = db.Column(db.Integer, primary_key=True)
    inviter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    invitee_username = db.Column(db.String(100), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('families.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())