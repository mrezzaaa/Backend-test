from flask_restful import Resource, reqparse
from flask import request
from marshmallow import ValidationError
from ..models.author import Author
from ..schemas.author import author_schema, authors_schema
from ..schemas.book import book_schema, books_schema
from ..extensions import db
import logging
class AuthorListResource(Resource):
    def get(self):
        try:
            authors = Author.query.all()
            result = {
                'items': authors_schema.dump(authors),
                'total': len(authors),
                'pages': 1,
                'page': 1
            }
            logging.info(f"GET /authors successful. Returning {len(authors)} authors.")
            return result, 200
        except Exception as e:
            logging.error(f"Error in GET /authors: {str(e)}")
            return {'message': 'An error occurred while fetching authors'}, 500
    
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            data = author_schema.load(json_data)
            author = Author(
                name=data['name'],
                bio=data.get('bio'),
                birth_date=data.get('birth_date')
            )
            db.session.add(author)
            db.session.commit()
            return author_schema.dump(author), 201
        except ValidationError  as err:
            return err.messages, 422

class AuthorResource(Resource):
    def get(self, author_id):
        author = Author.query.get_or_404(author_id)
        return author_schema.dump(author)

    def put(self, author_id):
        author = Author.query.get_or_404(author_id)
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            data = author_schema.load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 422
        for key, value in data.items():
            setattr(author, key, value)
        db.session.commit()
        return author_schema.dump(author)

    def delete(self, author_id):
        author = Author.query.get_or_404(author_id)
        db.session.delete(author)
        db.session.commit()
        return '', 204

class AuthorBooksResource(Resource):
    def get(self, author_id):
        author = Author.query.get_or_404(author_id)
        return books_schema.dump(author.books.all())
    





#This code defines three classes (AuthorListResource, AuthorResource, and AuthorBooksResource) 
#that handle RESTful API requests for managing authors and their books.

#AuthorListResource handles GET (retrieve all authors) and POST (create a new author) requests.
#AuthorResource handles GET (retrieve a single author), PUT (update an author), and DELETE (delete an author) requests.
#AuthorBooksResource handles GET (retrieve all books of an author) requests.
#Each class inherits from Resource and uses Flask-RESTful, Flask, and Marshmallow for API development, database interactions, and data validation, respectively. The code also includes error handling and logging for debugging purposes.