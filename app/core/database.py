import mongoengine

from os import getenv
from sys import stderr

class Database():

    __host : str = getenv('MONGO_DB_HOST')
    __user : str = getenv('MONGO_DB_USER')
    __pass : str = getenv('MONGO_DB_PASS')
    __db   : str = getenv('MONGO_DB_DATABASE')
    __auth_source : str = 'admin'

    def connect(self):
        try:
            mongoengine.connect(
                self.__db, 
                host=self.__host, 
                username=self.__user, 
                password=self.__pass,
                authentication_source=self.__auth_source
            )
        except Exception as e:
            print(e, file=stderr)
