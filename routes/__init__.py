from flask import Blueprint

# Create a Blueprint for books
books_bp = Blueprint('books', __name__)

from . import books
