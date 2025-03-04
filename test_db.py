from app import create_app
from app.extensions import db
from app.models import Category

app = create_app()

with app.app_context():
    print(Category.query.all())
