from marshmallow import Schema, fields

class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    bio = fields.Str()
    birth_date = fields.Date()

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)





#This code defines a schema for serializing and deserializing author data using the Marshmallow library.
#The AuthorSchema class defines the structure of the author data, with fields for id, name, bio, and birth_date. The id field is read-only (dump_only=True), and the name field is required.
#The code then creates two instances of the AuthorSchema class: author_schema for serializing a single author, and authors_schema for serializing multiple authors (many=True).