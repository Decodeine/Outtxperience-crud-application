from flask import Flask, request, jsonify
from flask_restx import Api, Resource, reqparse
from model import db, Book
from Schema import BookSchema
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

db.init_app(app)

book_schema = BookSchema()

api = Api(app, version='1.0', title='Book API', description='A simple crud operation Book API')

ns = api.namespace('books', description='Book operations')
#  a parser for the book data
book_parser = reqparse.RequestParser()
book_parser.add_argument('title', type=str, required=True, help='Title cannot be blank!')
book_parser.add_argument('author', type=str, required=True, help='Author cannot be blank!')

@ns.route('/')
class BookList(Resource):

    def get(self):
        #List all books
        all_books = Book.query.all()
        result = book_schema.dump(all_books, many=True)
        return jsonify(result),200

    @ns.expect(book_parser)
    def post(self):
    #Create a new book
       data = book_parser.parse_args()
       errors = book_schema.validate(data)
       if errors:
          return errors, 400

       new_book = Book(title=data['title'], author=data['author'])
       db.session.add(new_book)
       db.session.commit()
       return book_schema.dump(new_book), 201
    
@ns.route('/<int:book_id>')
class Book(Resource):
    
    def get(self, book_id):
        book = Book.query.get(book_id)
        if book:
            return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year, 'isbn': book.isbn}), 200
        else:
            return jsonify({'error': 'Book not found'}), 404

    @ns.expect(book_parser) 
    def put(self, book_id):
        book = Book.query.get(book_id)
        if book:
            data = book_parser.parse_args()
            errors = book_schema.validate(data, partial=True) 
            if errors:
                return jsonify(errors), 400
            for key, value in data.items():
                setattr(book, key, value)
            db.session.commit()
            return book_schema.dump(book), 200
        else:
            return jsonify({'error': 'Book not found'}), 404
        
    def delete(self, book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return jsonify({'status': 'Book deleted'}), 200
        else:
            return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)