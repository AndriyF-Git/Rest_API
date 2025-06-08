from flask import Flask, jsonify, request, abort
from dataclasses import dataclass, field
from marshmallow import ValidationError
from marshmallow_dataclass import class_schema
import itertools
from . import book_bp
import json

_id_gen = itertools.count(1)
@dataclass(order=True, frozen = True)
class Book:
    id: int = field(init=False)
    title: str
    author: str
    year: int

    def __post_init__(self):
        object.__setattr__(self, 'id', next(_id_gen))


BookSchemaClass = class_schema(Book)
BookSchema = BookSchemaClass()

initial_books = [
    {"title": "Dune", "author": "Frank Herbert", "year": 1965},
    {"title": "1984", "author": "George Orwell", "year": 1949}
]

books = []

try:
    for book_data in initial_books:
        book = BookSchema.load(book_data)
        books.append(book)
    print(books)
except ValidationError as err:
    print(err.messages)
    print(err.valid_data)


@book_bp.route('/', methods=['GET'])
def get_books():
    return jsonify(books), 200

@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if getattr(book, "id", None) == book_id:
            return jsonify(BookSchema.dump(book))
    return jsonify({"error": "Book not found"}), 404

@book_bp.route('/add_book', methods=['POST'])
def add_book():
    try:
        data = BookSchema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    books.append(data)
    return jsonify(data), 201

@book_bp.route('/delete/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    book_exists = any(book.id == book_id for book in books)
    if not book_exists:
        abort(404, description="Книгу не знайдено")
    books = [book for book in books if book.id != book_id]
    return jsonify({"message": "Книгу видалено"}), 200
