from todo_app.data.todo_items import Item
import os
import pymongo
from bson.objectid import ObjectId
import datetime

def get_connection():
    client = pymongo.MongoClient(os.getenv("COSMOS_CONNECTION_STRING"))
    endpoint = client
    return endpoint

def get_database():
    database = get_connection()
    database = database[os.getenv("DATABASE")]
    return database

def get_card_collection():
    database = get_database()
    cards = database.cards
    return cards

def get_items():
    """
    Fetches all saved items from the trello app for the specified board.
    Returns:
        items(cards) and their list(action, Not started, in progress and completed)
    """
    cards = get_card_collection()

    allCards = []
    for card in cards.find():
        allCards.append(Item.fromCard(card))
    return allCards

def get_item(card_id):
    cards = get_card_collection()
    return cards.find({"_id": ObjectId(card_id)})

def add_item(name, desc, due):
    """
    This function new task (name) as its parameter provided when the user submits new task. It reterives list 'not started' ID from get_list() function.
    """
    cards = get_card_collection()
    card = {
        "name": name,
        "desc": desc,
        "due": due,
        "dateLastActivity": datetime.datetime.utcnow(),
        "list": "Not Started"
    }
    cards.insert_one(card)
    return Item.fromCard(card)


def move_card_to_list(card_id, list):
    """
    This function moves a card to a list and takes the card id and list id as parameter from functions item_in_progress, item_completed & reset_item_status.
    """
    cards = get_card_collection()
    response = cards.update_one({'_id':ObjectId(card_id)}, {'$set':{'list':list, 'dateLastActivity': datetime.datetime.utcnow()}})
    return response


def item_in_progress(card_id):
    """
    This function gets the card id when the user wants to progress a item and calls the move_card_to_list function. 
    """
    card = move_card_to_list(card_id, 'In Progress') 
    return card

def item_completed(card_id):
    """
    This function gets the card id when the user completes a item and calls the move_card_to_list function. . 
    """
    card = move_card_to_list(card_id, 'Completed')
    return card

def reset_item_status(card_id):
    """
    This function gets the card id when the user wants to set the item to not started and calls the move_card_to_list function. . 
    """
    card = move_card_to_list(card_id,'Not Started')
    return card











