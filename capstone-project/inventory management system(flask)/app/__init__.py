from flask import Flask
import os
from app.utils.logging_config import setup_logging
from flask_sqlalchemy import SQLAlchemy

setup_logging()
app = Flask(__name__, template_folder='../templates',static_folder='../static')
app.secret_key = "My-Secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','mysql://root:root@localhost/world')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

from .models import db, User,Item
from .auth import *
from .main import *

with app.app_context():
    db.create_all()
    
    admin_user = User.query.filter_by(username='admin').first()
    if admin_user is None:
        admin_password = 'admin'
        admin_email = 'admin@nucleusteq.com'
        admin_user = User(username='admin', password=admin_password, email=admin_email, is_admin=True)
        db.session.add(admin_user)
        db.session.commit()