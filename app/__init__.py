from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    with app.app_context():
        from app import views

        from app.books.models import Book
        from .books import book_bp
        from app.books import views
        app.register_blueprint(book_bp)
        db.create_all()

    return app