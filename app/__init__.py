from flask import Flask
from flask_pymongo import MongoClient
from app.config import Config
from app.routes.sales import sales_blueprint
from app.routes.cards import cards_blueprint
from app.routes.main import main
from app.routes.cogs import cogs_blueprint
from app.routes.users import users_blueprint

# Create the Flask app instance
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db = Config.db

    # Register blueprints for different routes
    app.register_blueprint(main)
    app.register_blueprint(sales_blueprint, url_prefix='/sales')
    app.register_blueprint(users_blueprint, url_prefix='/users')
    app.register_blueprint(cogs_blueprint, url_prefix='/cogs')
    app.register_blueprint(cards_blueprint, url_prefix='/cards')

    app.db = db

    return app