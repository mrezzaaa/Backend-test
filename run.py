from app import create_app, db
from app.models.author import Author
from app.models.book import Book
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import OperationalError
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

app = create_app()

def create_db_if_not_exists(uri):
    db_name = uri.split('/')[-1]
    db_uri_without_name = '/'.join(uri.split('/')[:-1])
    
    try:
        if not database_exists(uri):
            # Connect to PostgreSQL server
            conn = psycopg2.connect(db_uri_without_name + '/postgres')
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Create the database
            cursor.execute(f'CREATE DATABASE {db_name}')
            
            # Close the connection
            cursor.close()
            conn.close()
            
            print(f"Database '{db_name}' created successfully.")
        else:
            print(f"Database '{db_name}' already exists.")
    except Exception as e:
        print(f"An error occurred while creating the database: {str(e)}")

def init_db():
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully.")
        except OperationalError:
            print("Failed to create tables. Attempting to create database...")
            create_db_if_not_exists(app.config['SQLALCHEMY_DATABASE_URI'])
            db.create_all()
            print("Database and tables created successfully.")

if __name__ == '__main__':
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    init_db()
    app.run(host='0.0.0.0',port=9000,debug=True)
    print(f"Server running on http://localhost:9000")



#This code is used to initialize a Flask application with a PostgreSQL database.

#Here's what it does:

#It creates a Flask application instance using the create_app function.
#It defines two functions: create_db_if_not_exists and init_db.
#create_db_if_not_exists checks if a database exists at a given URI. If it doesn't, it creates the database.
#init_db creates all tables in the database. If it fails due to the database not existing, it calls create_db_if_not_exists to create the database and then tries again.
#Finally, it prints the database URI, initializes the database, and runs the Flask application in debug mode.
#This code is typically used in a development environment to ensure the database and tables are created when the application starts.







