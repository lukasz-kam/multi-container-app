import pytest
import os
from app import create_app
from flask import json
from pymongo import MongoClient
from bson import ObjectId

@pytest.fixture
def client():
    app = create_app('test')
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mongodb():
    mongo_ip = os.getenv('MONGO_IP', 'localhost:27017')
    client = MongoClient(f'mongodb://{mongo_ip}/')
    db = client['todoapp_test']
    todos_collection = db['todos']

    todos_collection.drop()

    yield todos_collection

    todos_collection.drop()

def test_get_all_todos(client, mongodb):
    response = client.get('/todos')

    assert response.status_code == 200
    assert response.json == []

def test_create_todo(client, mongodb):
    new_todo = {
        'title': 'Test Todo',
        'description': 'This is a test todo',
        'completed': False
    }
    response = client.post('/todos', json=new_todo)
    data = response.json
    todo_id = data['id']
    todo_from_db = mongodb.find_one({'_id': ObjectId(todo_id)})

    assert response.status_code == 201
    assert todo_from_db is not None
    assert todo_from_db['title'] == new_todo['title']
    assert todo_from_db['description'] == new_todo['description']
    assert todo_from_db['completed'] == new_todo['completed']


def test_get_todo_by_id(client, mongodb):
    todo = {
        'title': 'Test Todo',
        'description': 'This is a test todo',
        'completed': False
    }
    result = mongodb.insert_one(todo)
    todo_id = str(result.inserted_id)
    response = client.get(f'/todos/{todo_id}')
    data = response.json

    assert response.status_code == 200
    assert data['id'] == todo_id
    assert data['title'] == todo['title']

def test_update_todo(client, mongodb):
    todo = {
        'title': 'Test Todo',
        'description': 'This is a test todo',
        'completed': False
    }
    result = mongodb.insert_one(todo)
    todo_id = str(result.inserted_id)

    updated_todo = {
        'title': 'Updated Todo',
        'description': 'Updated description',
        'completed': True
    }
    response = client.put(f'/todos/{todo_id}', json=updated_todo)
    data = response.json

    assert response.status_code == 200
    assert data['id'] == todo_id
    assert data['title'] == updated_todo['title']
    assert data['description'] == updated_todo['description']
    assert data['completed'] == updated_todo['completed']

def test_delete_todo(client, mongodb):
    todo = {
        'title': 'Test Todo',
        'description': 'This is a test todo',
        'completed': False
    }
    result = mongodb.insert_one(todo)
    todo_id = str(result.inserted_id)
    response = client.delete(f'/todos/{todo_id}')
    todo_in_db = mongodb.find_one({'_id': result.inserted_id})

    assert response.status_code == 200
    assert response.json['message'] == "Todo deleted"
    assert todo_in_db is None

def test_get_todo_by_id_not_found(client):
    response = client.get('/todos/123456789012345678901234')

    assert response.status_code == 404
    assert response.json['error'] == 'Todo not found'

def test_delete_todo_not_found(client):
    response = client.delete('/todos/123456789012345678901234')

    assert response.status_code == 404
    assert response.json['error'] == 'Todo not found'
