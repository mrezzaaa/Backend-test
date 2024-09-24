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

@pytest.fixture
def author(client):
    response = client.post('/authors', json={
        'name': 'J.K. Rowling',
        'bio': 'British author',
        'birth_date': '1965-07-31'
    })
    return json.loads(response.data)

def test_create_book(client, author):
    response = client.post('/books', json={
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'description': 'The first book in the Harry Potter series',
        'publish_date': '1997-06-26',
        'author_id': author['id']
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Harry Potter and the Philosopher\'s Stone'
    assert data['author_id'] == author['id']

def test_get_books(client, author):
    client.post('/books', json={
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'description': 'The first book in the Harry Potter series',
        'publish_date': '1997-06-26',
        'author_id': author['id']
    })
    response = client.get('/books')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'items' in data
    assert len(data['items']) == 1
    assert data['items'][0]['title'] == 'Harry Potter and the Philosopher\'s Stone'
    assert 'total' in data
    assert 'pages' in data
    assert 'page' in data

def test_get_book(client, author):
    response = client.post('/books', json={
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'description': 'The first book in the Harry Potter series',
        'publish_date': '1997-06-26',
        'author_id': author['id']
    })
    book_id = json.loads(response.data)['id']
    response = client.get(f'/books/{book_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Harry Potter and the Philosopher\'s Stone'

def test_update_book(client, author):
    response = client.post('/books', json={
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'description': 'The first book in the Harry Potter series',
        'publish_date': '1997-06-26',
        'author_id': author['id']
    })
    book_id = json.loads(response.data)['id']
    response = client.put(f'/books/{book_id}', json={
        'description': 'Updated description'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['description'] == 'Updated description'

def test_delete_book(client, author):
    response = client.post('/books', json={
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'description': 'The first book in the Harry Potter series',
        'publish_date': '1997-06-26',
        'author_id': author['id']
    })
    book_id = json.loads(response.data)['id']
    response = client.delete(f'/books/{book_id}')
    assert response.status_code == 204
    response = client.get(f'/books/{book_id}')
    assert response.status_code == 404