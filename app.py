from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer , primary_key=True,unique=True)
    title =db.Column(db.String(50), nullable = False)
    author = db.Column(db.String(50),nullable = False)
    year = db.Column(db.Integer,nullable = True)
    isbn = db.Column(db.String(50),nullable=True)

@app.route('/books', methods=['POST'])
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

@app.route('/books', methods=['GET'])
def index():
    books = Book.query.all()
    output = []
    for book in books:
        output.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn
        })
    return jsonify(output)

@app.route('/books/<int:id>', methods=['GET']) 
def get_book(id):
    book = Book.query.filter_by(id=id).first()
    if book is None:
        return jsonify({"message": "Book not found"}), 404
    
    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn
    })

@app.route('/books/<int:id>', methods=['PUT']) 
def update_book(id):
    data = request.json
    book = Book.query.filter_by(id=id).first()
    
    if book is None:
        return jsonify({"message": "Book not found"}), 404

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.year = data.get('year', book.year)
    book.isbn = data.get('isbn', book.isbn)
    
    db.session.commit()
    
    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn
    })


@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    db.session.query(Book).filter(Book.id == id).delete()
    db.session.commit()
    return jsonify({"message": "Book has been deleted successfully!"}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)