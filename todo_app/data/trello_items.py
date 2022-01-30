from todo_app.data.todo_items import Item
import requests, os
from dotenv import load_dotenv

load_dotenv()

def get_auth_params():
    """
    Returns the key and token required to get access to your Trello account

    """
    auth_params = {'key': os.getenv("TRELLO_API_KEY"), 'token': os.getenv("TRELLO_TOKEN")}

    return auth_params


def build_url(endpoint):
    """
    This function builds the complete url for required endpoint

    """
    return os.getenv("TRELLO_BASE_URL") + endpoint

def build_params(params={}):
    full_params = get_auth_params()
    full_params.update(params)
    return full_params

def get_lists():
    """
    This function gets all open cards and its list for the specified board.
    
    """
    params = build_params({'cards': 'open'})
    url = build_url('/boards/%s/lists' % os.getenv("TRELLO_BOARD_ID"))
    response = requests.get(url, params = params)
    print(response)
    lists = response.json()
    return lists

def get_list(name):
    lists = get_lists()
    return next((list for list in lists if list['name'] == name), None)

def get_items():
    """
    Fetches all saved items from the trello for the specified board.

    Returns:
        items(cards) and their list(action, Not started, in progress and completed)
    
    """
    lists = get_lists()
    items = []
    for card_list in lists:
        for card in card_list['cards']:
            items.append(Item.fromTrelloCard(card, card_list))
    return items


def add_item(name):
    todo_list = get_list('Not Started')
    url = build_url('/cards')
    params = build_params({'name': name, 'idList':todo_list['id']})
    response = requests.post(url, params = params)
    card = response.json()
    return Item.fromTrelloCard(card, todo_list)













