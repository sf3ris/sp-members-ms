from flask import Flask, make_response, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from routes import routes, members_routes, membership_routes, athlete_routes
from core.bootstrap import Bootstrap
from core.database import Database

from middlewares.auth_middleware import AuthMiddleware

load_dotenv()

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={
    r'/*': {
        'origins': [
            'http://localhost:3001'
        ]
    }
})

app.wsgi_app = AuthMiddleware(app.wsgi_app)

app.register_blueprint(routes.routes)
app.register_blueprint(members_routes.member_routes)
app.register_blueprint(membership_routes.membership_routes)
app.register_blueprint(athlete_routes.athlete_routes)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(401)
def not_found(error):
    return make_response(jsonify({'error': 'Unauthorized'}), 401)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

if __name__ == "__main__":
    Bootstrap()
    app.run(host="0.0.0.0", debug=True, port=5001)