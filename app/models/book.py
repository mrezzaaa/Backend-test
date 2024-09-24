from ..extensions import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    publish_date = db.Column(db.Date)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'
    





#This code defines a Book class that represents a database table using SQLAlchemy, a Python SQL toolkit. 
# The class has five columns: 
# id : number
# title : string 
# description : text 
# publish_date : date
# author_id : number 
# 
# The author_id column is a foreign key referencing the id column of an author table. 
# The repr method returns a string representation of a Book object, displaying its title.