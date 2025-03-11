import os
from app.routes.transactions import main_routes 
from datetime import timedelta
from flask import Flask
from dotenv import load_dotenv
from app.config import Config
from app.extensions import db, migrate
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_cors import CORS

load_dotenv()  # Load environment variables from .env file

def create_app():
    app = Flask(__name__)
    
    # Load configuration from Config class
    app.config.from_object(Config)

    # Ensure DATABASE_URL is set in the environment and configure the database URI
    if 'DATABASE_URL' in os.environ:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace('postgres://', 'postgresql://')
    elif not app.config.get('SQLALCHEMY_DATABASE_URI'):
        raise ValueError("Either 'SQLALCHEMY_DATABASE_URI' or 'DATABASE_URL' must be set in the environment")

    # Initialize extensions
    CORS(app, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)

    # Session config
    app.config['SESSION_TYPE'] = 'sqlalchemy'  
    app.config['SESSION_SQLALCHEMY'] = db
    app.config['SESSION_PERMANENT'] = True  
    app.config['SESSION_USE_SIGNER'] = True  
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_COOKIE_SECURE'] = False 

    Session(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.transactions import transactions_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_routes)
    app.register_blueprint(transactions_bp, url_prefix='/transactions')

    # Create all tables (for local testing)
    with app.app_context():
        db.create_all()

    return app

# Create app instance
app = create_app()
