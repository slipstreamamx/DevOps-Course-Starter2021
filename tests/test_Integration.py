import os
from urllib import response
import pytest
import requests
from todo_app import app
from dotenv import load_dotenv, find_dotenv

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data
    
    def json(self): 
        return self.fake_response_data
    
def stub(url, params):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    fake_response_data = None

    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = sample_trello_lists_response
        return StubResponse(fake_response_data)
    
    if url == f'https://api.trello.com/1/cards':
        fake_response_data = create_trello_card = {
    "id": not_started_item_id,
    "name": "Create a Task'",
    "idShort": "7",
    "desc": "Another Task",
    "due": "2022-05-28T15:48:26.091Z",
    "dateLastActivity": "2022-04-20T15:48:26.091Z",
    
}
        return StubResponse(fake_response_data)
    
    raise Exception(f'Integration test stub no mock for url "{url}"')


def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', stub)
    response = client.get('/')

    assert response.status_code == 200
    assert 'Task 2' in response.data.decode()

def test_add_item(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', stub)
    monkeypatch.setattr(requests, 'post', stub)
    response = client.post('/items/new', data=form_data)

    assert response.status_code == 302

not_started_list_id = '61b443bf6833200579c4e6b3'
in_progress_list_id = '61b443a067b68f6bb1b0896b'
completed_list_id = '61b442c18fd9bd14ca8bcb9b'

not_started_item_id = '61f24b80f5b18b1b900f314b'
in_progress_item_id = '61b5b5b46779504b27126c2b'
completed_item_id = '5ee100cac4bbbf5bd0350b3f'

sample_trello_lists_response = [
    {
        "id": not_started_list_id,
        "name": "Not Started",
        "cards": [
            {
                "id": not_started_item_id,
                "idShort": "2",
                "name": "Task 2",
                "desc": "Task 2 not started",
                "due": "2022-05-28T15:48:26.091Z",
                "dateLastActivity": "2022-04-10T15:48:26.091Z",
            }
        ]
    },
    {
        "id": in_progress_list_id,
        "name": "In Progress",
        "cards": [
            {
                "id": in_progress_item_id,
                "idShort": "3",
                "name": "Task 3",
                "desc": "Task 3 in progress",
                "due": "2022-05-20T15:48:26.091Z",
                "dateLastActivity": "2022-04-10T15:48:26.091Z",
            }
        ]
    },
    {
        "id": completed_list_id,
        "name": "Completed",
        "cards": [
            {
                "id": completed_item_id,
                "idShort": "6",
                "name": "Task 6",
                "desc": "Task 6 completed",
                "due": "2022-03-20T15:48:26.091Z",
                "dateLastActivity": "2022-03-20T15:48:26.091Z",
            }
        ]
    }
]

sample_trello_card = {
    "id": not_started_item_id,
    "idShort": "2",
    "name": "Task 2",
    "desc": "Task 2 not started",
    "due": "2022-05-28T15:48:26.091Z",
}

form_data = {'name': 'Create a Task', 'desc text': 'Another Task', 'date': '2022-05-28T15:48:26.091Z'}




