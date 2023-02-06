"""
A file that defines the classes stored in the database.
"""

import uuid
import enum
from datetime import datetime
from persistent import Persistent
from dataclasses import dataclass, field
import pytz


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

    item: int
    quantity: int
    stackSize: int
    price: float
    total: float
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
    A category of items. The Default category has the id 0.

    Attributes:
        id: the id of the category
        name: the name of the category
    """

    id: int = field(init=False)
    name: str

    def __post_init__(self):
        self.id = uuid.uuid4().int
        if self.name == "Default":
            self.id = 0


def process_timestamp(timestamp: int) -> datetime:
    """
    Converts the timestamp to a datetime object.

    Arguments:
        timestamp {int} -- The timestamp to convert.

    Returns:
        datetime -- The datetime object.
    """
    delta = timestamp
    # TODO find a way to get the timezone from the user, probably using the user's locale or a setting
    tz = pytz.timezone("Europe/Zurich")
    date = datetime.fromtimestamp(delta, tz=tz)
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


def extract_item_id(item: str) -> int:
    """
    Extracts the item id from the item string.

    Arguments:
        item {str} -- The item string. Has the following format: "i:item_id"

    Returns:
        int -- The item id.
    """
    return int(item.split(":")[1])


def get_correct_source(source: str) -> Source:
    """
    Returns the correct source based on the source string.

    Arguments:
        source {str} -- The source string.

    Returns:
        Source -- The correct source.

    Raises:
        ValueError: If the source string is invalid.
    """
    if source == "Auction":
        return Source.AUCTION
    elif source == "Vendor":
        return Source.VENDOR
    else:
        raise ValueError(f"Invalid source: {source}")
