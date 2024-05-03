from flask import Flask, request, jsonify
from model import db, Book
from Schema import BookSchema
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

db.init_app(app)

book_schema = BookSchema()

with app.app_context():
    db.create_all()
@app.route('/books', methods=['POST'])
def create_book():
    errors = book_schema.validate(request.json)
    if errors:
        return jsonify(errors), 400
    new_book = Book(**request.json)
    db.session.add(new_book)
    db.session.commit()
    return book_schema.dump(new_book), 201

@app.route('/books', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year, 'isbn': book.isbn} for book in all_books]), 200

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year, 'isbn': book.isbn}), 200
    else:
        return jsonify({'error': 'Book not found'}), 404

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if book:
        errors = book_schema.validate(request.json, partial=True) 
        if errors:
            return jsonify(errors), 400
        for key, value in request.json.items():
            setattr(book, key, value)
        db.session.commit()
        return book_schema.dump(book), 200
    else:
        return jsonify({'error': 'Book not found'}), 404
    
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'status': 'Book deleted'}), 200
    else:
        return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)