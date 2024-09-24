from marshmallow import Schema, fields

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    publish_date = fields.Date()
    author_id = fields.Int(required=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)



#This code defines a schema for serializing and deserializing book data using the Marshmallow library.

#The BookSchema class defines the structure of the book data, with fields for:
#id: number
#title:  string
#description:  string
#publish_date: date
#author_id:  number


#Two instances of the schema are created:
#book_schema: for serializing a single book
#books_schema: for serializing multiple books (many=True)