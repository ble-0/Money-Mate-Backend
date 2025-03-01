from flask import Flask
from app.extensions import db
from app.routes.auth import auth_bp
from app.routes.transactions import transactions_bp
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    migrate = Migrate(app, db)

    # Import analytics routes AFTER initializing db
    from app.routes.analytics import analytics_bp  

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(transactions_bp, url_prefix="/transactions")
    app.register_blueprint(analytics_bp, url_prefix="/analytics") 

    return app

