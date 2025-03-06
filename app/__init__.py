from flask import flask
from flask_session import session
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config
from app.extensions import db, migrate
from app.models.category import Category
from app.models.transaction import Transaction
from app.models.user import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    #Enable CORS for all routes
    CORS(app, supports_credentials=True)

    # Set the session file directory to a folder inside the instance directory
    app.config['SESSION_FILE_DIR'] = os.path.join(app.instance_path, 'flask_session')

    # Initialize JWTManager
    jwt = JWTManager(app)

    # Initialize Flask-Session
    app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the filesystem
    app.config['SESSION_FILE_DIR'] = session_dir # Directory for session files
    app.config['SESSION_PERMANENT'] = False  # Sessions are not permanent
    app.config['SESSION_USE_SIGNER'] = True  # Sign the session cookie
    Session(app)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app.routes import main, transactions, auth, analytics

        app.register_blueprint(main.main_bp)
        app.register_blueprint(transactions.transactions_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(analytics.analytics_bp)

    return app
    
app = create_app()