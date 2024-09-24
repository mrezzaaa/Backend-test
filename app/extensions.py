from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


#This code initializes two Flask extensions:
#SQLAlchemy: an ORM (Object-Relational Mapping) tool for interacting with a database.
#Marshmallow: a library for serializing and deserializing data to/from JSON.
#The db and ma objects are instances of these extensions, 
# which can be used to interact with the database and serialize/deserialize data, respectively.