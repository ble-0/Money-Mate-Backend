import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get absolute path of the project
    INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')  # Path to the instance directory
    DATABASE_URL = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(INSTANCE_DIR, 'money_mate.db')}")

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1')
    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

    @staticmethod
    def ensure_instance_folder():
        """Ensure the instance folder exists to prevent SQLite errors."""
        if not os.path.exists(Config.INSTANCE_DIR):
            os.makedirs(Config.INSTANCE_DIR)

# Ensure the instance folder exists at runtime
Config.ensure_instance_folder()
