import os
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

    #Enable CORS for all routes
    CORS(app, supports_credentials=True)

    # Set the session file directory to a folder inside the instance directory
    app.config['SESSION_FILE_DIR'] = os.path.join(app.instance_path, 'flask_session')


    # Initialize Flask-Session
    session_dir = os.path.join(app.instance_path, 'flask_session')  # Define session_dir
    os.makedirs(session_dir, exist_ok=True)  # Create the directory if it doesn't exist
    app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the filesystem
    app.config['SESSION_FILE_DIR'] = session_dir # Directory for session files
    app.config['SESSION_PERMANENT'] = False  # Sessions are not permanent
    app.config['SESSION_USE_SIGNER'] = True  # Sign the session cookie
    app.config['SESSION_COOKIE_SECURE'] = True  # Secure the session cookie
    Session(app)

    db.init_app(app)
    migrate.init_app(app, db)



    app.register_blueprint(auth_bp)
    app.register_blueprint(transactions_bp, url_prefix='/transactions')

    with app.app_context():
        db.create_all()

    return app
    
app = create_app()