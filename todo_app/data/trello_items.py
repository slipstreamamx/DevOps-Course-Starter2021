from todo_app.data.todo_items import Item
from datetime import date, datetime
import os
import pymongo
from bson.objectid import ObjectId

def get_connection():
    endpoint = pymongo.MongoClient(os.getenv("COSMOS_CONNECTION_STRING"))

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
    Fetches all cards.
    Returns:
        list: The list of cards.
    """
    cards = get_card_collection()

    allCards = []
    for card in cards.find():
        allCards.append(Item.fromCard(card))
    return allCards

def get_item(id):
    cards = get_card_collection()
    return cards.find({"_id": ObjectId(id)})

def add_item(name, desc, due):
    """
    Adds a new card with the specified name.
    Args:
        name: The name of the card.
        desc: The description of the card
        due: due date of the card
    """
    cards = get_card_collection()
    card = {
        "name": name,
        "desc": desc,
        "due": due,
        "last_modified": datetime.now(),
        "list": "Not Started"
    }
    cards.insert_one(card)
    return Item.fromCard(card)


def move_card_to_list(id, list):
    """
    Runs a put request to update the card list
    Args:
        id: The ID of the card to be updated
        list: The list object to use for the new list
    Returns: 
        card: The updated card, in the new specified list
    """
    cards = get_card_collection()
    response = cards.update_one({'_id': ObjectId(id)}, {'$set': {'list': list, 'last_modified': datetime.now()}})
    return response


def item_in_progress(id):
    """
    Moves the card with the specified ID to the "In Progress" list.
    Args:
        id (str): The ID of the card.
    Returns:
        card: The saved card, or None if no cards match the specified ID.
    """
    card = move_card_to_list(id, 'In Progress') 
    return card

def item_completed(id):
    """
    Moves the item with the specified ID to the "Completed" list.
    Args:
        id (str): The ID of the card.
    Returns:
        card: The saved card, or None if no cards match the specified ID.
    """
    card = move_card_to_list(id, 'Completed')
    return card

def reset_item_status(id):
    """
    Moves the item with the specified ID to the "Not Started" list.
    Args:
        id (str): The ID of the card.
    Returns:
        card: The saved card, or None if no cards match the specified ID.
    """
    card = move_card_to_list(id,'Not Started')
    return card











