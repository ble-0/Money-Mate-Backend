from flask import Flask
from flask_migrate import Migrate
from app.extensions import db
from app import create_app

app = create_app()

# Initialize Flask-Migrate
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)
