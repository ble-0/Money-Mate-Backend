import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get absolute path of the project
    
    DATABASE_URL = os.getenv('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1')
    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
