"""
The main part of the backend, which handles requests from the frontend and accesses the database.
"""

from .database import add_new_item, add_new_purchase, add_new_sale
import pandas as pd
from .models import Purchase, Sale, extract_item_id, process_price, process_timestamp, get_correct_source, Source


def check_if_transaction_is_acceptable(item_name: str, source: Source) -> bool:
    """
    Checks if a transaction is acceptable. Are currently skipped :
        - transactions with a source of "Vendor"
        - transactions with an item name of "?"

    Arguments:
        item_name {str} -- The name of the item.
        source {Source} -- The source of the transaction.

    Returns:
        bool -- True if the transaction is acceptable, False otherwise.
    """
    # if sale is to a vendor, or if name == '?', ignore it
    if source == Source.VENDOR or item_name == "?":
        return False
    return True


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

        # if transaction is not acceptable, ignore it
        if not check_if_transaction_is_acceptable(itemName, source):
            continue

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

        # if transaction is not acceptable, ignore it
        if not check_if_transaction_is_acceptable(itemName, source):
            continue

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

        # if item not in database, add it
        add_new_item(itemId, itemName)

        result.append(sale)
    return result


def insert_purchases(purchases: list[Purchase]) -> None:
    """
    Inserts the purchases into the database.

    Arguments:
        purchases {list[Purchase]} -- The purchases to insert.
    """
    for purchase in purchases:
        add_new_purchase(purchase)


def insert_sales(sales: list[Sale]) -> None:
    """
    Inserts the sales into the database.

    Arguments:
        sales {list[Sale]} -- The sales to insert.
    """
    for sale in sales:
        add_new_sale(sale)
