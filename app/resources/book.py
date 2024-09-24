from flask_restful import Resource,reqparse
from flask import request
from ..models.book import Book
from ..schemas.book import book_schema, books_schema
from ..extensions import db
from marshmallow import ValidationError
import logging

class BookListResource(Resource):
    # Run the all book query, accessing them with a GET request http://localhost:5000/books
    def get(self):
        try:
            books = Book.query.all()
            result = {
                'items': books_schema.dump(books),
                'total': len(books),
                'pages': 1,
                'page': 1
            }
            logging.info(f"GET /books successful. Returning {len(books)} books.")
            return result, 200
        except Exception as e:
            logging.error(f"Error in GET /books: {str(e)}")
            return {'message': 'An error occurred while fetching books'}, 500

    #Inserting a new book with a POST request http://localhost:5000/books
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            data = book_schema.load(json_data)
            book = Book(
                title=data['title'],
                description=data.get('description'),
                publish_date=data.get('publish_date'),
                author_id=data['author_id']
            )
            db.session.add(book)
            db.session.commit()
            return book_schema.dump(book), 201
        except ValidationError as err:
            return err.messages, 422

class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        return book_schema.dump(book)

    def put(self, book_id):
        book = Book.query.get_or_404(book_id)
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            data = book_schema.load(json_data, partial=True)
            for key, value in data.items():
                setattr(book, key, value)
            db.session.commit()
            return book_schema.dump(book)
        except ValidationError as err:
            return err.messages, 422

    def delete(self, book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return '', 204
    



# This code defines two classes, BookListResource and BookResource, which handle RESTful API requests for managing books.

#BookListResource handles:
#   GET /books: Retrieves a list of all books, returning a JSON response with the books' data, total count, and pagination information.
#   POST /books: Creates a new book based on the provided JSON data, validating the input using a schema and returning the created book's data or an error message.

#BookResource handles:
#   GET /books/:book_id: Retrieves a single book by its ID, returning the book's data or a 404 error if not found.
#   PUT /books/:book_id: Updates an existing book's data based on the provided JSON data, validating the input using a schema and returning the updated book's data or an error message.
#   DELETE /books/:book_id: Deletes a book by its ID, returning an empty response with a 204 status code.
#   The code uses Flask-RESTful, Flask, and Marshmallow for API development, database interactions, and data validation, respectively.







