from flask import Flask
from flask_migrate import Migrate  
from app.extensions import db, bcrypt, jwt
from app.models import User, Transaction
from app.routes import auth_bp, transactions_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/money-mate.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db) 

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(transactions_bp, url_prefix='/transactions')

    return app
