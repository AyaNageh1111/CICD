from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import json
from datetime import datetime

class Product(db.Model):
    __seachbale__ = ['name','desc']
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(3000), nullable=False)
    Price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.String(3), default="No")
    stock = db.Column(db.Integer, nullable=False)
    description= db.Column(db.Text, nullable=False)
    colors = db.Column(db.Text, nullable=True)
    date_modified = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    Producer=db.Column(db.String(3000), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))
    Admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3000), unique=True, nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3000), unique=True, nullable=False)

class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedDict)
    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice

# class Cart(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     Products= db.Column(db.List, db.ForeignKey('user.id'))
#     Total_price= id = db.Column(db.Integer)
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    products = db.relationship('Product')
    notes = db.relationship('Note')