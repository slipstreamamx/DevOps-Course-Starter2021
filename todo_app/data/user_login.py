import requests
import os


state = os.getenv("STATE")

def build_url(endpoint):
    return os.getenv("GET_USER_IDENTITY_URL") + endpoint


def get_user_identity_endpoint():
    
    url = build_url('/authorize?' + 'client_id=' + os.getenv("CLIENT_ID") + '&state=' + os.getenv("STATE"))

    return url

def get_access_token_endpoint(request_token: str) -> str:

    url = build_url('/access_token?' + 'client_id=' + os.getenv("CLIENT_ID") + '&client_secret=' + os.getenv("CLIENT_SECRET") + '&code=' + {request_token})

    headers = {

        'accept': 'application/json'
    }

    response = requests.post(url, headers=headers)

    data = response.json()

    access_token = data['access_token']

    return access_token

def get_user_data_endpoint(access_token):

    access_token = 'token ' + access_token

    url = os.getenv("GET_USER_URL")

    headers = {"Authorization": access_token}

    response = requests.get(url=url, headers=headers)

    userData = response.json()

    return userData