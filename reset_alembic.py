from app import create_app
from app.extensions import db
from sqlalchemy import text  # Import text()

app = create_app()

with app.app_context():
    db.session.execute(text("DROP TABLE IF EXISTS alembic_version;"))
    db.session.commit()
    print("Dropped alembic_version table successfully.")
