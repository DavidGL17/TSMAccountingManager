"""
A file that defines the classes stored in the database.
"""

import uuid
import enum
from persistent import Persistent
from dataclasses import dataclass


class Source(enum.Enum):
    AUCTION = 1
    VENDOR = 2


@dataclass
class Purchase(Persistent):
    stackSize: int  # how many items are in a stack
    quantity: int  # the total number of items
    price: float  # needs to be converted from copper to gold
    item: int  # reference to item
    source: Source


@dataclass
class Sale(Persistent):
    stackSize: int  # how many items are in a stack
    quantity: int  # the total number of items
    price: float  # needs to be converted from copper to gold
    item: int  # reference to item
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
