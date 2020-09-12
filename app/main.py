from flask import Flask
from routes import routes, members_routes
from core.bootstrap import Bootstrap
from core.database import Database

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(routes.routes)
app.register_blueprint(members_routes.member_routes)

if __name__ == "__main__":
    Bootstrap()
    app.run(host="0.0.0.0", debug=True, port=5001)