from ZODB import DB
import os
from persistent.dict import PersistentDict
import transaction
from .models import Category, Item, Purchase, Sale


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
            self.dbroot["app_data"] = PersistentDict()
            self.dbroot["app_data"]["items"] = PersistentDict()
            self.dbroot["app_data"]["categories"] = PersistentDict()
            self.dbroot["app_data"]["purchases"] = PersistentDict()
            self.dbroot["app_data"]["sales"] = PersistentDict()

            # add a default category
            category = Category(name="Default")
            self.dbroot["app_data"]["categories"][str(category.id)] = category
            transaction.commit()


zodb = SingletonZODB.instance()


def check_item_exists(item_id: int) -> bool:
    """
    Checks if an item exists in the database.

    Arguments:
        item_id {int} -- The id of the item.

    Returns:
        bool -- True if the item exists, False otherwise.
    """
    return str(item_id) in zodb.dbroot["app_data"]["items"]


def add_new_item(item_id: int, item_name: str) -> bool:
    """
    Adds a new item to the database.If the item already exists, it will not be added.
    By default the Category is set to the "Default" category.

    Arguments:
        item_id {int} -- The id of the item.
        item_name {str} -- The name of the item.


    Returns:
        bool -- True if the item was added, False otherwise.
    """
    if check_item_exists(item_id):
        return False
    zodb.dbroot["app_data"]["items"][str(item_id)] = Item(
        id=item_id, name=item_name, category=zodb.dbroot["app_data"]["categories"].get("0").id
    )
    transaction.commit()
    return True


def add_new_purchase(purchase: Purchase) -> bool:
    """
    Adds a new purchase to the database.

    Arguments:
        purchase {Purchase} -- The purchase to add.

    Returns:
        bool -- True if the purchase was added, False otherwise.
    """
    # Check if the expense already exists
    if str(purchase.id) in zodb.dbroot["app_data"]["purchases"]:
        return False
    # Add the purchase
    zodb.dbroot["app_data"]["purchases"][str(purchase.id)] = purchase
    transaction.commit()
    return True


def add_new_sale(sale: Sale) -> bool:
    """
    Adds a new sale to the database.

    Arguments:
        sale {Sale} -- The sale to add.

    Returns:
        bool -- True if the sale was added, False otherwise.
    """
    # Check if the sale already exists
    if str(sale.id) in zodb.dbroot["app_data"]["sales"]:
        return False
    zodb.dbroot["app_data"]["sales"][str(sale.id)] = sale
    transaction.commit()
    return True
