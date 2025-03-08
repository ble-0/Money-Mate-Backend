import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get absolute path of the project
    INSTANCE_DIR = os.path.join(BASE_DIR,'..', 'instance')  # Path to the instance directory
    DATABASE_URL = os.getenv('DATABASE_URL',"postgresql://money_mate_db_user:OQVveuBE79DKAOz2KEN0szI5zf5Lh6IX@dpg-cv69re2j1k6c73e3no1g-a/money_mate_db")

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1')
    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
