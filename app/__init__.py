from flask import Flask
from flask_pymongo import MongoClient
from app.config import Config
from app.routes.sales import sales_blueprint
from app.routes.accounts import accounts
from app.routes.products import products_blueprint
from app.routes.main import main

# Create the Flask app instance
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db = Config.db

    # Register blueprints for different routes
    app.register_blueprint(main)
    app.register_blueprint(sales_blueprint, url_prefix='/sales')
    app.register_blueprint(accounts)
    app.register_blueprint(products_blueprint, url_prefix='/products')

    app.db = db

    return app