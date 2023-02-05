"""
A file that defines the classes stored in the database.
"""

import uuid
import enum
from datetime import datetime
from persistent import Persistent
from dataclasses import dataclass
import pandas as pd


class Source(enum.Enum):
    AUCTION = 1
    VENDOR = 2


@dataclass
class Purchase(Persistent):
    stackSize: int  # how many items are in a stack
    quantity: int  # the total number of items
    price: float  # the price of a single item, needs to be converted from copper to gold
    total: float  # the total price of the sale, quantity * price
    item: int  # reference to item
    time: datetime  # the time the purchase was made
    source: Source


@dataclass
class Sale(Persistent):
    stackSize: int  # how many items are in a stack
    quantity: int  # the total number of items
    price: float  # the price of a single item, needs to be converted from copper to gold
    total: float  # the total price of the sale, quantity * price
    item: int  # reference to item
    time: datetime  # the time the purchase was made
    source: Source


@dataclass
class Item(Persistent):
    id: int
    name: str
    category: int


@dataclass
class Category(Persistent):
    id: int
    name: str

    def __post_init__(self):
        self.id = uuid.uuid4().int


def process_timestamp(timestamp: int) -> datetime:
    """
    Converts the timestamp to a datetime object.

    Arguments:
        timestamp {int} -- The timestamp to convert.

    Returns:
        datetime -- The datetime object.
    """
    delta = timestamp
    date = datetime.fromtimestamp(delta)
    return date


def process_price(price: int, quantity: int) -> tuple[float, float]:
    """
    Converts the price from copper to gold, and returns the total price based on the quantity.

    Arguments:
        price {int} -- The price of a single item in copper.
        quantity {int} -- The total number of items.

    Returns:
        float -- The price of a single item in gold.
        float -- The total price of the sale.
    """
    gold = price / 10000
    total = gold * quantity
    return gold, total


def process_expenses(expenses: pd.DataFrame) -> list[Purchase]:
    """
    Processes the expenses dataframe and returns a list of purchases.

    Arguments:
        expenses {pd.DataFrame} -- The expenses dataframe.

    Returns:
        list[Purchase] -- A list of purchases.
    """
    # TODO create function once the database is set up
    pass


def process_revenue(revenue: pd.DataFrame) -> list[Sale]:
    """
    Processes the revenue dataframe and returns a list of sales.

    Arguments:
        revenue {pd.DataFrame} -- The revenue dataframe.

    Returns:
        list[Sale] -- A list of sales.
    """
    # TODO create function once the database is set up
    pass
