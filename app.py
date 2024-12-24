from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from config import Config
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
api = Api(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    isbn = db.Column(db.String(50), nullable=True)

class BookSchema(Schema):
    title = fields.Str(required=True, validate=lambda x: len(x) > 1 and len(x) <= 50)
    author = fields.Str(required=True, validate=lambda x: len(x) > 1 and len(x) <= 50)
    year = fields.Int(validate=lambda x: -1000 <= x <= 9999, required=False)
    isbn = fields.Str(validate=lambda x: len(x) >= 10 and len(x) <= 14, required=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route('/books', methods=['POST'])
def add_book():
    try:
        data = book_schema.load(request.json) 
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    new_book = Book(**data)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"message": "Book added", "id": new_book.id}), 201

@app.route('/books', methods=['GET'])
def index():
    books = Book.query.all()
    return jsonify(books_schema.dump(books))

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.filter_by(id=id).first()
    if book is None:
        return jsonify({"message": "Book not found"}), 404
    return jsonify(book_schema.dump(book))

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.filter_by(id=id).first()
    if book is None:
        return jsonify({"message": "Book not found"}), 404

    try:
        data = book_schema.load(request.json)  # Validate and parse data
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.year = data.get('year', book.year)
    book.isbn = data.get('isbn', book.isbn)
    
    db.session.commit()
    
    return jsonify(book_schema.dump(book))

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    db.session.query(Book).filter(Book.id == id).delete()
    db.session.commit()
    return jsonify({"message": "Book has been deleted successfully!"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
