from flask import Flask
from flask_pymongo import PyMongo
from .config import SECRET_KEY, MONGO_URI
from .routes import main

mongo = None

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['MONGO_URI'] = MONGO_URI
    
    global mongo
    mongo = PyMongo(app)

    app.register_blueprint(main)
    from .routes import accounts
    app.register_blueprint(accounts, url_prefix="/accounts")

    return app