from ZODB import DB
import os
from persistent.mapping import PersistentMapping
import transaction
from .models import Category


class SingletonZODB:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        # check if data folder exists, otherwise create it
        if not os.path.exists("data"):
            os.mkdir("data")
        self.db = DB("data/data.fs")
        self.conn = self.db.open()
        self.dbroot = self.conn.root()

        if "app_data" not in self.dbroot:
            print("Initializing database...")
            # init the database
            self.dbroot["app_data"] = PersistentMapping()
            self.dbroot["app_data"]["items"] = PersistentMapping()
            self.dbroot["app_data"]["categories"] = PersistentMapping()
            self.dbroot["app_data"]["purchases"] = PersistentMapping()
            self.dbroot["app_data"]["sales"] = PersistentMapping()

            # add a default category
            self.dbroot["app_data"]["categories"]["default"] = Category(name="Default")
            transaction.commit()


zodb = SingletonZODB.instance()
