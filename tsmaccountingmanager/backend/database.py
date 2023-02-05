"""
The main part of the backend, which handles requests from the frontend and connects to the database
"""

from ZODB import DB
from persistent.mapping import PersistentMapping


class SingletonZODB:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.db = DB("data.fs")
        self.conn = self.db.open()
        self.dbroot = self.conn.root()

        if "app_data" not in self.dbroot:
            self.dbroot["app_data"] = PersistentMapping()


zodb = SingletonZODB.instance()
