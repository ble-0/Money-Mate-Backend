
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app import routes

# Create database and JWT manager instances
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)

    # App configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(routes)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
