from flask import Flask
from flask_restful import Api
from .extensions import db, ma
from config import Config
from .errors import register_error_handlers  # Add this import
from flask_caching import Cache
from flask_profiler import Profiler


cache = Cache()
profiler = Profiler()
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app, config=app.config)

    # Setup flask-profiler
    app.config["flask_profiler"] = {
        "enabled": app.config["DEBUG"],
        "storage": {
            "engine": "sqlite"
        },
        "basicAuth":{
            "enabled": True,
            "username": "admin",
            "password": "admin"
        },
        "ignore": [
            "^/static/.*"
        ]
    }
    profiler = Profiler()  # You can have this in another module
    profiler.init_app(app)
    # Register error handlers
    register_error_handlers(app)

    # Initialize API
    api = Api(app)

    # Import and register resources
    from .resources.author import AuthorResource, AuthorListResource, AuthorBooksResource
    from .resources.book import BookResource, BookListResource

    api.add_resource(AuthorListResource, '/authors')
    api.add_resource(AuthorResource, '/authors/<int:author_id>')
    api.add_resource(AuthorBooksResource, '/authors/<int:author_id>/books')
    api.add_resource(BookListResource, '/books')
    api.add_resource(BookResource, '/books/<int:book_id>')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app




#This code defines a function create_app that initializes a Flask web application with the following components:

#Configures the app with settings from the Config class
#Initializes database and marshmallow extensions
#Registers error handlers
#Sets up a RESTful API with resources for authors and books
#Creates database tables
#The function returns the fully configured Flask app instance.