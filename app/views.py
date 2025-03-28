from flask import Flask, jsonify, request, abort
from marshmallow import Schema, fields, ValidationError
from . import app
import uuid




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


# 🔧 Обробка помилок
@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


