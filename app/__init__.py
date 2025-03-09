import os
from datetime import timedelta
from flask import Flask
from flask_session import Session
from flask_cors import CORS
from app.config import Config
from app.extensions import db, migrate
from app.models.transaction import Transaction
from app.models.user import User
from app.routes.auth import auth_bp
from app.routes.transactions import transactions_bp
from app.routes import main, transactions, auth, analytics

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    if os.environ.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace('postgres://','postgresql://')

    CORS(app, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)


    app.config['SESSION_TYPE'] = 'sqlalchemy'  
    app.config['SESSION_SQLALCHEMY'] = db
    app.config['SESSION_PERMANENT'] = True  
    app.config['SESSION_USE_SIGNER'] = True  
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_COOKIE_SECURE'] = False 

    Session(app)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(transactions_bp, url_prefix='/transactions')

    with app.app_context():
        db.create_all()

    return app
    
app = create_app()