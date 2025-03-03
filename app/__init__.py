from flask import Flask
from flask_migrate import Migrate
from app.extensions import db
from app.routes import transactions_bp, auth_bp  # Import blueprints

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/money_mate.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate (app, db)

    # Register Blueprints
    app.register_blueprint(transactions_bp, url_prefix="/transactions")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
