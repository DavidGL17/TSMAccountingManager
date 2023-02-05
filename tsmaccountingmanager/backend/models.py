"""
A file that defines the classes stored in the database.
"""

import uuid
import enum
from datetime import datetime
from persistent import Persistent
from dataclasses import dataclass, field


class Source(enum.Enum):
    AUCTION = 1
    VENDOR = 2


@dataclass
class Purchase(Persistent):
    """
    A purchase made in the game.

    Attributes:
        stackSize: how many items are in a stack
        quantity: the total number of items
        price: the price of a single item, needs to be converted from copper to gold
        total: the total price of the sale, quantity * price
        item: reference to the item (as an id)
        time: the time the purchase was made
        source: the source of the purchase
    """

    stackSize: int
    quantity: int
    price: float
    total: float
    item: int
    time: datetime
    source: Source


@dataclass
class Sale(Persistent):
    """
    A sale made in the game.

    Attributes:
        stackSize: how many items are in a stack
        quantity: the total number of items
        price: the price of a single item, needs to be converted from copper to gold
        total: the total price of the sale, quantity * price
        item: reference to the item (as an id)
        time: the time the purchase was made
        source: the source of the purchase
    """

    stackSize: int
    quantity: int
    price: float
    total: float
    item: int
    time: datetime
    source: Source


@dataclass
class Item(Persistent):
    """
    An item in the game.

    Attributes:
        id: the id of the item
        name: the name of the item
        category: the category of the item
    """

    id: int
    name: str
    category: int


@dataclass
class Category(Persistent):
    """
    A category of items.

    Attributes:
        id: the id of the category
        name: the name of the category
    """

    id: int = field(init=False)
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
