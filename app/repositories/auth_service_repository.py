from requests import post
from os import getenv
from sys import stderr

class AuthServiceRepository():

    def __init__(self):
        self.__host = getenv('AUTH_SERVICE_HOST')

    def validate_token(self, token : str ) -> bool:

        endpoint = self.__host + '/validate'
        body = { 'access_token' : token }

        response = post( endpoint, body)

        print(response.text, file=stderr)

        return True if response.status_code == 200 else False