from flask import Flask, make_response, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from routes import routes, members_routes, membership_routes
from core.bootstrap import Bootstrap
from core.database import Database

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

app.register_blueprint(routes.routes)
app.register_blueprint(members_routes.member_routes)
app.register_blueprint(membership_routes.membership_routes)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    Bootstrap()
    app.run(host="0.0.0.0", debug=True, port=5001)