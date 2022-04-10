from todo_app.data.todo_items import Item
import requests, os

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
    This function gets all lists and their open cards for specified board.
    """
    params = build_params({'cards': 'open'})
    url = build_url('/boards/%s/lists' % os.getenv("TRELLO_BOARD_ID"))
    response = requests.get(url, params = params)
    print(response)
    lists = response.json()
    return lists

def get_list(name):
    """
    This function gets the lists for specified board and then returns the list name provided in the parameter.
    """
    lists = get_lists()
    return next((list for list in lists if list['name'] == name), None)

def get_items():
    """
    Fetches all saved items from the trello app for the specified board.
    Returns:
        items(cards) and their list(action, Not started, in progress and completed)
    """
    lists = get_lists()
    items = []
    for card_list in lists:
        for card in card_list['cards']:
            items.append(Item.fromTrelloCard(card, card_list))
    return items

def add_item(name, desc, due):
    """
    This function new task (name) as its parameter provided when the user submits new task. It reterives list 'not started' ID from get_list() function.
    """
    todo_list = get_list('Not Started')
    url = build_url('/cards')
    params = build_params({'name': name, 'desc': desc, 'due':due, 'idList':todo_list['id']})
    response = requests.post(url, params = params)
    card = response.json()
    return Item.fromTrelloCard(card, todo_list)

def move_card_to_list(card_id, list):
    """
    This function moves a card to a list and takes the card id and list id as parameter from functions item_in_progress, item_completed & reset_item_status.
    """
    url = build_url('/cards/%s' % card_id)
    params = build_params({'idList': list['id']})
    response = requests.put(url, params=params)
    card = response.json()
    return card

def item_in_progress(id):
    """
    This function gets the card id when the user wants to progress a item and calls the move_card_to_list function. 
    """
    doing_list = get_list('In Progress')
    card = move_card_to_list(id, doing_list) 
    return Item.fromTrelloCard(card, doing_list)

def item_completed(id):
    """
    This function gets the card id when the user completes a item and calls the move_card_to_list function. . 
    """
    done_list = get_list('Completed')
    card = move_card_to_list(id, done_list)
    return Item.fromTrelloCard(card, done_list)

def reset_item_status(id):
    """
    This function gets the card id when the user wants to set the item to not started and calls the move_card_to_list function. . 
    """
    todo_list = get_list('Not Started')
    card = move_card_to_list(id,todo_list)
    return Item.fromTrelloCard(card, todo_list)













