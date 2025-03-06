from app import create_app

app = create_app()

app.register_blueprint(transactions_bp, url_prefix='/transactions')


if __name__ == "__main__":
    app.run(debug=TRUE)
