from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(3000))
    Price=db.Column(db.Float)
    Producer=db.Column(db.String(3000))
    date_modified = db.Column(db.DateTime(timezone=True), default=func.now())
    Admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description= db.Column(db.String(20000))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    products = db.relationship('Product')
