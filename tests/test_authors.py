import json
import pytest
from app import create_app, db
from app.models.author import Author
from app.models.book import Book
from datetime import date
from flask_caching import Cache

@pytest.fixture
def client():
    app = create_app('config.TestConfig')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_create_author(client):
    response = client.post('/authors', json={
        'name': 'J.K. Rowling',
        'bio': 'British author',
        'birth_date': '1965-07-31'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'J.K. Rowling'
    assert data['bio'] == 'British author'
    assert data['birth_date'] == '1965-07-31'

def test_get_authors(client):
    client.post('/authors', json={
        'name': 'J.K. Rowling',
        'bio': 'British author',
        'birth_date': '1965-07-31'
    })
    response = client.get('/authors')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'items' in data
    assert len(data['items']) == 1
    assert data['items'][0]['name'] == 'J.K. Rowling'
    assert 'total' in data
    assert 'pages' in data
    assert 'page' in data

def test_get_author(client):
    response = client.post('/authors', json={
        'name': 'J.K. Rowling',
        'bio': 'British author',
        'birth_date': '1965-07-31'
    })
    author_id = json.loads(response.data)['id']
    response = client.get(f'/authors/{author_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'J.K. Rowling'

def test_update_author(client):
    response = client.post('/authors', json={
        'name': 'J.K. Rowling',
        'bio': 'British author',
        'birth_date': '1965-07-31'
    })
    author_id = json.loads(response.data)['id']
    response = client.put(f'/authors/{author_id}', json={
        'bio': 'Updated bio'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['bio'] == 'Updated bio'

def test_delete_author(client):
    response = client.post('/authors', json={
        'name': 'J.K. Rowling',
        'bio': 'British author',
        'birth_date': '1965-07-31'
    })
    author_id = json.loads(response.data)['id']
    response = client.delete(f'/authors/{author_id}')
    assert response.status_code == 204
    response = client.get(f'/authors/{author_id}')
    assert response.status_code == 404

def test_get_author_books(client):
    # Create an author
    author_response = client.post('/authors', json={
        'name': 'J.K. Rowling',
        'bio': 'British author',
        'birth_date': '1965-07-31'
    })
    author_id = json.loads(author_response.data)['id']

    # Create a book for the author
    book_response = client.post('/books', json={
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'description': 'The first book in the Harry Potter series',
        'publish_date': '1997-06-26',
        'author_id': author_id
    })
    assert book_response.status_code == 201

    # Get the author's books
    response = client.get(f'/authors/{author_id}/books')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['title'] == 'Harry Potter and the Philosopher\'s Stone'