# Creating the database models
from email.policy import default
from . import db
from flask_login import UserMixin

class App(db.Model):
    id = id = db.Column(db.Integer, primary_key= True)
    name  = db.Column(db.String(150))
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    user_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique= True)
    password = db.Column(db.String(150))
    secret_key = db.Column(db.String(500))
    
    apps = db.relationship('App')

    activate_key = db.Column(db.Boolean(), default= False)




