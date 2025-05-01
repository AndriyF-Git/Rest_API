from flask import Flask, jsonify, request, abort
from marshmallow import Schema, fields, ValidationError
import uuid
from . import book_bp
from .models import Book
from app import db

class BookSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    year = fields.Int(required=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)


@book_bp.route('/', methods=['GET'])
def get_books():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    books = Book.query.limit(limit).offset(offset).all()
    results = [{"id": b.id, "title": b.title, "author": b.author} for b in books]
    return jsonify(results), 200

@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404, description="Book not found")
    return jsonify({"id": book.id, "title": book.title, "author": book.author}), 200

@book_bp.route('/add_book', methods=['POST'])
def add_book():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('author'):
        abort(400, description="Missing data")

    book = Book(title=data['title'], author=data['author'])
    db.session.add(book)
    db.session.commit()
    return jsonify({"id": book.id, "title": book.title, "author": book.author}), 201

@book_bp.route('/delete/<string:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404, description="Book not found")
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"}), 200
