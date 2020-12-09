from flask_login import UserMixin
from datetime import datetime
from . import db

# documentation: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    estate = db.Column(db.String(100))
    # maybe add another field here to display budget
    budget = db.Column(db.String(100))
    remaining = db.Column(db.String(100))
    # maybe need to add functions to allow users to manually renew their budget
    # add income function to the main.py
    profile_pic = db.Column(db.String(100))
    items = db.relationship('Item', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.name)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.String(100))
    link = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Item {}>'.format(self.name)