from flask import Flask, Request, Response, abort, jsonify
from repositories.auth_service_repository import AuthServiceRepository

from typing import Dict, Any
from sys import stderr

class AuthMiddleware():

    BEARER_TOKEN_TYPE = 'Bearer'

    def __init__(self, app : Flask):
        self.__app = app

    def __call__(self, environ , start_response) : 
        request = Request( environ )
        if(request.method == 'OPTIONS'): return self.__app(environ, start_response)

        token = request.headers.get('Authorization')
        if(token is None): return self.send_unauthorized_response(environ, start_response)

        [ tokentype, token ] = token.split(' ')
        if( tokentype is None or tokentype != self.BEARER_TOKEN_TYPE or token is None ): return self.send_unauthorized_response(environ, start_response)
        
        if( not AuthServiceRepository().validate_token(token)):
            return self.send_unauthorized_response(environ, start_response)
        else:
            return self.__app(environ, start_response)
        
    def send_unauthorized_response( self, environ, start_response):
            response = Response(u'Authorization failed', mimetype= 'text/plain', status=401)
            return response(environ, start_response)