from flask import Flask, jsonify, request, abort
from marshmallow import Schema, fields, ValidationError
import uuid
from . import book_bp

# 📚 Симуляція бази даних
books = []


# ✅ Схема для валідації книги
class BookSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    year = fields.Int(required=True)


book_schema = BookSchema()
books_schema = BookSchema(many=True)

@book_bp.route('/')
def index():
    return "Hello"

# 🟢 Отримати всі книги
@book_bp.route('/books', methods=['GET'])
def get_books():
    return jsonify(books_schema.dump(books)), 200


# 🟢 Отримати книгу за ID
@book_bp.route('/books/<string:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if not book:
        abort(404, description="Книгу не знайдено")
    return jsonify(book_schema.dump(book)), 200


# 🟢 Додати нову книгу
@book_bp.route('/books', methods=['POST'])
def add_book():
    try:
        data = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    data['id'] = str(uuid.uuid4())  # Генеруємо унікальний ID
    books.append(data)
    return jsonify(book_schema.dump(data)), 201


# 🟢 Видалити книгу
@book_bp.route('/books/<string:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    book = next((book for book in books if book['id'] == book_id), None)
    if not book:
        abort(404, description="Книгу не знайдено")

    books = [b for b in books if b['id'] != book_id]
    return jsonify({"message": "Книгу видалено"}), 200

