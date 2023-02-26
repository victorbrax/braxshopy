from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///braxshopy.db"
app.config['SECRET_KEY'] = 'OFlamengoEhBomDemais2023'
db.init_app(app)  
bcrypt = Bcrypt(app)

from shop.admin import routes