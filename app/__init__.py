from flask import Flask
from flask_pymongo import PyMongo
from .config import SECRET_KEY, MONGO_URI

mongo = None

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['MONGO_URI'] = MONGO_URI
    
    global mongo
    mongo = PyMongo(app)

    from .routes.main import main
    app.register_blueprint(main)

    return app