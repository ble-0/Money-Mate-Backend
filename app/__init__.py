from flask import Flask
from app.config import Config
from app.extensions import db, migrate
from app.models.category import Category
from app.models.transaction import Transaction
from app.models.user import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

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