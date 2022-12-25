import requests
import os

class UserAccess:

    def get_access_token(request_token):

        if not request_token:
            raise ValueError('The request token is mandatory!')
        if not isinstance(request_token, str):
            raise ValueError('The request token nust be a string!')

        url = 'https://github.com/login/oauth/access_token?' + 'client_id=' + str(os.getenv("CLIENT_ID")) + '&client_secret=' + str(os.getenv("CLIENT_SECRET")) + '&code=' + str(request_token)

        headers = {

            'accept': 'application/json'
        }

        response = requests.post(url, headers=headers)

        data = response.json()

        access_token = data['access_token']

        return access_token

    def get_user_data(access_token):

        access_token = 'token ' + access_token

        url = 'https://api.github.com/user'

        headers = {"Authorization": access_token}

        response = requests.get(url=url, headers=headers)

        userData = response.json()

        return userData
    