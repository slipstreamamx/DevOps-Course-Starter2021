import requests
import os
import string, random

def build_url(endpoint):
    return str(os.getenv("GET_USER_IDENTITY_URL")) + endpoint


def get_user_identity_endpoint():
    
    state_string  = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    url = build_url('/authorize?' + 'client_id=' + str(os.getenv("CLIENT_ID")) + '&state=' + str(state_string))

    return url

def get_access_token_endpoint(request_token):

    if not request_token:
        raise ValueError('The request token is mandatory!')
    if not isinstance(request_token, str):
        raise ValueError('The request token nust be a string!')

    url = build_url('/access_token?' + 'client_id=' + str(os.getenv("CLIENT_ID")) + '&client_secret=' + str(os.getenv("CLIENT_SECRET")) + '&code=' + str(request_token))

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