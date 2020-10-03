
import flask 
from typing import List

routes = flask.Blueprint('routes',__name__)

@routes.route('/', methods=["GET"])
def home( ) -> flask.Response :  

    return flask.jsonify("Welcome to Members Microservices API")