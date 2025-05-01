from flask import Flask, jsonify, request, abort, current_app
from marshmallow import Schema, fields, ValidationError
import uuid

@current_app.route('/')
def index():
    return "Hello"


# 🔧 Обробка помилок
@current_app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


@current_app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


