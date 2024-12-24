# app/routes/books.py

from flask import jsonify, request
from app import db
from models import Book
from . import bp

@bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author} for book in books])

@bp.route('/books', methods=['POST'])
def add_book():
    data = request.json
    title = data.get('title')
    author = data.get('author')
    year = data.get('year')
    isbn = data.get('isbn')

    new_book = Book(title=title, author=author, year=year, isbn=isbn)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"message": "Book added", "id": new_book.id}), 201
