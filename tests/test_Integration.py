import os
from urllib import response
import pytest
import requests
from todo_app import app
from dotenv import load_dotenv, find_dotenv
import mongomock
import pymongo


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def test_index_page(client):
    collection = pymongo.MongoClient(os.getenv("COSMOS_CONNECTION_STRING"))
    database = os.getenv("DATABASE")
    
    collection[database].cards.insert_many(sample_card_lists_response)
    
    response = client.get('/')
    
    assert response.status_code == 200
    assert 'Task 2' in response.data.decode()


def test_add_item(client):
    collection = pymongo.MongoClient(os.getenv("COSMOS_CONNECTION_STRING"))
    database = os.getenv("DATABASE")

    collection[database].cards.insert_many(sample_card_lists_response)

    response = client.get('/')

    collection[database].cards.insert_one(create_card)
        
    response = client.post('/items/new', data=form_data)

    assert response.status_code == 302


sample_card_lists_response = [
{
    "_id": "636278348df33aa5804e3f45",
    "name": "Task 2",
    "desc": "Task 2 not started",
    "due": "2022-05-28",
    "last_modified": mongomock.utcnow(),
    "list": "Not Started",
},
{
    "_id": "736278348df33aa5804e3f95",
    "name": "Task 3",
    "desc": "Task 3 in progress",
    "due": "2022-05-28",
    "last_modified": mongomock.utcnow(),
    "list": "In Progress",
},
{
    "_id": "836278348df33aa5804e3f88",
    "name": "Task 4",
    "desc": "Task 4 completed",
    "due": "2022-05-28",
    "last_modified": mongomock.utcnow(),
    "list": "Completed",
}
]

form_data = {'name': 'Create a Task', 'desc text': 'Another Task', 'date': '2022-05-28'}

create_card = {
    "_id": "446278348df33aa5804e3f95",
    "name": "Create a Task",
    "desc": "Another Task",
    "due": "2022-05-28",
    "last_modified": mongomock.utcnow(),
    "list": "Not Started",
}

