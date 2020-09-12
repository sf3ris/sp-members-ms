from core.database import Database
from dotenv import load_dotenv

class Bootstrap():

    def __init__(self):
        load_dotenv()
        Database().connect()