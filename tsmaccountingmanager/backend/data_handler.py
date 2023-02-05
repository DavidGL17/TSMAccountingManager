"""
The main part of the backend, which handles requests from the frontend and accesses the database.
"""

from .database import zodb
import pandas as pd
from .models import Purchase, Sale


def process_expenses(expenses: pd.DataFrame) -> list[Purchase]:
    """
    Processes the expenses dataframe and returns a list of purchases.

    Arguments:
        expenses {pd.DataFrame} -- The expenses dataframe.

    Returns:
        list[Purchase] -- A list of purchases.
    """
    zodb.dbroot
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
