from todo_app.data.todo_items import Item
from urllib import response
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
    params = build_params({'cards': 'open'})
    url = build_url('/boards/%s/lists' % os.getenv("TRELLO_BOARD_ID"))
    response = requests.get(url, params = params)
    lists = response.json()
    return lists

def get_items():
    lists = get_lists()
    items = []
    for card_list in lists:
        for card in card_list['cards']:
            items.append(Item.fromTrelloCard(card, card_list))
    print(items)
    return items
get_items()












