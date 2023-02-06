"""
The main part of the backend, which handles requests from the frontend and accesses the database.
"""

from .database import add_new_item
import pandas as pd
from .models import Purchase, Sale, extract_item_id, process_price, process_timestamp, get_correct_source


def process_expenses(expenses: pd.DataFrame) -> list[Purchase]:
    """
    Processes the expenses dataframe and returns a list of purchases.

    Arguments:
        expenses {pd.DataFrame} -- The expenses dataframe.

    Returns:
        list[Purchase] -- A list of purchases.
    """
    result = []
    # process the dataframe
    for index, row in expenses.iterrows():
        itemId = extract_item_id(row["itemString"])
        itemName = row["itemName"]
        stackSize = row["stackSize"]
        quantity = row["quantity"]
        price, total = process_price(row["price"], stackSize)
        time = process_timestamp(row["time"])
        source = get_correct_source(row["source"])

        # if item not in database, add it
        add_new_item(itemId, itemName)

        # create the purchase
        purchase = Purchase(
            item=itemId,
            stackSize=stackSize,
            quantity=quantity,
            price=price,
            total=total,
            time=time,
            source=source,
        )
        result.append(purchase)
    return result


def process_sales(sales: pd.DataFrame) -> list[Sale]:
    """
    Processes the sales dataframe and returns a list of sales.

    Arguments:
        sales {pd.DataFrame} -- The sales dataframe.

    Returns:
        list[Sale] -- A list of sales.
    """
    result = []
    # process the dataframe
    for index, row in sales.iterrows():
        itemId = extract_item_id(row["itemString"])
        itemName = row["itemName"]
        stackSize = row["stackSize"]
        quantity = row["quantity"]
        price, total = process_price(row["price"], stackSize)
        time = process_timestamp(row["time"])
        source = get_correct_source(row["source"])

        # if item not in database, add it
        add_new_item(itemId, itemName)

        # create the sale
        sale = Sale(
            item=itemId,
            stackSize=stackSize,
            quantity=quantity,
            price=price,
            total=total,
            time=time,
            source=source,
        )
        result.append(sale)
    return result
