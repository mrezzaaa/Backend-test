from ..extensions import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    birth_date = db.Column(db.Date)
    books = db.relationship('Book', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<Author {self.name}>'
    




#This code defines a class Author that represents a database table using SQLAlchemy, a Python SQL toolkit.
#The class has five attributes:

#   id: a unique integer primary key
#   name: a string with a maximum length of 100 characters that cannot be null
#   bio: a text field for the author's biography
#   birth_date: a date field for the author's birthdate
#   books: a relationship with the Book class, indicating that an author can have multiple books
#The repr method returns a string representation of the author, showing their name.