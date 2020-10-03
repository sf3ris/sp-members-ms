from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from routes import routes, members_routes
from core.bootstrap import Bootstrap
from core.database import Database

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(routes.routes)
app.register_blueprint(members_routes.member_routes)

if __name__ == "__main__":
    Bootstrap()
    app.run(host="0.0.0.0", debug=True, port=5001)