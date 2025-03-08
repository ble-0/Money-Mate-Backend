from app import create_app
from app.routes.transactions import transactions_bp

app = create_app()

app.register_blueprint(transactions_bp, url_prefix='/transactions')


if __name__ == "__main__":
    app.run(debug=True)
