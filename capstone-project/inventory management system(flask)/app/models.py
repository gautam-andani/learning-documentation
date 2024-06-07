from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

from . import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'  # default tablename will be smallcase classname user
    
    username = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    is_admin = db.Column(db.String(255), default=False)
    first_login = db.Column(db.String(255), default=True)
    

class Item(db.Model):
    __tablename__ = 'items'
    
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(255), nullable=False)
    serial_number = db.Column(db.Integer,unique=True)
    bill_no = db.Column(db.Integer, nullable=False)
    date_of_purchase = db.Column(db.Date, nullable=True)
    assigned_to = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=True)
    warranty = db.Column(db.Date, nullable=True)
    
    user = relationship("User", backref="items")