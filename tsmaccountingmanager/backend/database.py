from ZODB import DB
import os
from persistent.dict import PersistentDict
import transaction
from .models import Category, Item, Purchase, Sale
from datetime import datetime


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


###
# Insertion
###


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


def add_new_category(category: Category) -> bool:
    """
    Adds a new category to the database.

    Arguments:
        category {Category} -- The category to add.

    Returns:
        bool -- True if the category was added, False otherwise.
    """
    # Check if the category already exists
    if str(category.id) in zodb.dbroot["app_data"]["categories"]:
        return False
    zodb.dbroot["app_data"]["categories"][str(category.id)] = category
    transaction.commit()
    return True


###
# Get
###

# Purchases


def get_purchases() -> list:
    """
    Gets all purchases.

    Returns:
        list -- A list of purchases.
    """
    return list(zodb.dbroot["app_data"]["purchases"].values())


def get_purchases_by_time(start: datetime, end: datetime) -> list:
    """
    Gets all purchases between the start and end time.

    Arguments:
        start {datetime} -- The start time.
        end {datetime} -- The end time.

    Returns:
        list -- A list of purchases.
    """
    filtered_purchases = [
        purchase for purchase in zodb.dbroot["app_data"]["purchases"].values() if start <= purchase.time <= end
    ]
    return filtered_purchases


def get_purchases_by_item(item_id: int) -> list:
    """
    Gets all purchases for a specific item.

    Arguments:
        item_id {int} -- The id of the item.

    Returns:
        list -- A list of purchases.
    """
    filtered_purchases = [
        purchase for purchase in zodb.dbroot["app_data"]["purchases"].values() if purchase.item == item_id
    ]
    return filtered_purchases


def get_purchases_by_category(category_id: int) -> list:
    """
    Gets all purchases for a specific category.

    Arguments:
        category_id {int} -- The id of the category.

    Returns:
        list -- A list of purchases.
    """
    filtered_purchases = [
        purchase
        for purchase in zodb.dbroot["app_data"]["purchases"].values()
        if zodb.dbroot["app_data"]["items"][str(purchase.item)].category == category_id
    ]
    return filtered_purchases


# Sales


def get_sales() -> list:
    """
    Gets all sales.

    Returns:
        list -- A list of sales.
    """
    return list(zodb.dbroot["app_data"]["sales"].values())


def get_sales_by_time(start: datetime, end: datetime) -> list:
    """
    Gets all sales between the start and end time.

    Arguments:
        start {datetime} -- The start time.
        end {datetime} -- The end time.

    Returns:
        list -- A list of sales.
    """
    filtered_sales = [sale for sale in zodb.dbroot["app_data"]["sales"].values() if start <= sale.time <= end]
    return filtered_sales


def get_sales_by_item(item_id: int) -> list:
    """
    Gets all sales for a specific item.

    Arguments:
        item_id {int} -- The id of the item.

    Returns:
        list -- A list of sales.
    """
    filtered_sales = [sale for sale in zodb.dbroot["app_data"]["sales"].values() if sale.item == item_id]
    return filtered_sales


def get_sales_by_category(category_id: int) -> list:
    """
    Gets all sales for a specific category.

    Arguments:
        category_id {int} -- The id of the category.

    Returns:
        list -- A list of sales.
    """
    filtered_sales = [
        sale
        for sale in zodb.dbroot["app_data"]["sales"].values()
        if zodb.dbroot["app_data"]["items"][str(sale.item)].category == category_id
    ]
    return filtered_sales


# Items


def get_items() -> list:
    """
    Gets all items.

    Returns:
        list -- A list of items.
    """
    return list(zodb.dbroot["app_data"]["items"].values())


def get_item_by_id(item_id: int) -> Item:
    """
    Gets an item by its id.

    Arguments:
        item_id {int} -- The id of the item.

    Returns:
        Item -- The item.
    """
    return zodb.dbroot["app_data"]["items"].get(str(item_id))


def get_items_by_category(category_id: int) -> list[Item]:
    """
    Gets all items for a specific category.

    Arguments:
        category_id {int} -- The id of the category.

    Returns:
        list -- A list of items.
    """
    filtered_items = [item for item in zodb.dbroot["app_data"]["items"].values() if item.category == category_id]
    return filtered_items


# Categories


def get_categories() -> list:
    """
    Gets all categories.

    Returns:
        list -- A list of categories.
    """
    return list(zodb.dbroot["app_data"]["categories"].values())


def get_category_by_id(category_id: int) -> Category:
    """
    Gets a category by its id.

    Arguments:
        category_id {int} -- The id of the category.

    Returns:
        Category -- The category.
    """
    return zodb.dbroot["app_data"]["categories"].get(str(category_id))


###
# Delete functions
###


def delete_element(type: str, id: int):
    """
    Deletes an element from the database.

    Arguments:
        type {str} -- The type of the element. Can be "items", "categories", "purchases" or "sales".
        id {int} -- The id of the element.
    """
    if type in ["items", "categories", "purchases", "sales"]:
        if str(id) in zodb.dbroot["app_data"][type]:
            del zodb.dbroot["app_data"][type][str(id)]
            transaction.commit()


def delete_elements(type: str, ids: list[int]):
    """
    Deletes multiple elements from the database.

    Arguments:
        type {str} -- The type of the elements. Can be "items", "categories", "purchases" or "sales".
        ids {list[int]} -- A list of the ids of the elements.
    """
    if type in ["items", "categories", "purchases", "sales"]:
        for id in ids:
            if str(id) in zodb.dbroot["app_data"][type]:
                del zodb.dbroot["app_data"][type][str(id)]
        transaction.commit()
