from flask import Flask, jsonify, request, abort
from marshmallow import Schema, fields, ValidationError
import uuid

app = Flask(__name__)

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

@app.route('/')
def index():
    return "Hello"

# 🟢 Отримати всі книги
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books_schema.dump(books)), 200


# 🟢 Отримати книгу за ID
@app.route('/books/<string:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if not book:
        abort(404, description="Книгу не знайдено")
    return jsonify(book_schema.dump(book)), 200


# 🟢 Додати нову книгу
@app.route('/books', methods=['POST'])
def add_book():
    try:
        data = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    data['id'] = str(uuid.uuid4())  # Генеруємо унікальний ID
    books.append(data)
    return jsonify(book_schema.dump(data)), 201


# 🟢 Видалити книгу
@app.route('/books/<string:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    book = next((book for book in books if book['id'] == book_id), None)
    if not book:
        abort(404, description="Книгу не знайдено")

    books = [b for b in books if b['id'] != book_id]
    return jsonify({"message": "Книгу видалено"}), 200


# 🔧 Обробка помилок
@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


# ▶️ Запуск
if __name__ == '__main__':
    app.run(debug=True)
