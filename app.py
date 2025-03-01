
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.routes  import routes  

app = Flask(__name__)
app.register_blueprint(routes)  

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  

# Initialize database and JWT manager
db = SQLAlchemy(app)
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(debug=True)

from app import routes
from app.routes import *



