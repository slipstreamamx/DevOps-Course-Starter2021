from urllib import response
import requests, os
from dotenv import load_dotenv
load_dotenv()


board_id = os.getenv("TRELLO_BOARD_ID")


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


def get_list_of_boards():
    params = get_auth_params()
    url = build_url('/members/me/boards?fields=name,url')
    response = requests.get(url, params=params)
    boards_info =  response.json()
    return boards_info


get_list_of_boards()






