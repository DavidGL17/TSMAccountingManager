"""
The main part of the backend, which handles requests from the frontend and accesses the database.
"""

from .database import add_new_item, add_new_purchase, add_new_sale
import pandas as pd
from .models import Purchase, Sale, extract_item_id, process_price, process_timestamp, get_correct_source, Source
from ..utils.logger import logger


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
    Processes the expenses dataframe and adds them to the database.
    Adds new items to the database if they are not already in it. Returns a list of purchases.

    Arguments:
        expenses {pd.DataFrame} -- The expenses dataframe.

    Returns:
        list[Purchase] -- A list of purchases.
        int -- The number of purchases added to the database.
    """
    logger.info("Processing new expenses...")
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

    ctr = 0
    for purchase in result:
        if add_new_purchase(purchase):
            ctr += 1

    logger.info(f"Finished processing new expenses. Added {ctr} new purchases.")

    return result, ctr


def process_sales(sales: pd.DataFrame) -> list[Sale]:
    """
    Processes the sales dataframe and adds them to the database.
    Adds new items to the database if they are not already in it. Returns a list of sales.

    Arguments:
        sales {pd.DataFrame} -- The sales dataframe.

    Returns:
        list[Sale] -- A list of sales.
        int -- The number of sales added to the database.
    """
    logger.info("Processing new sales...")
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
    ctr = 0
    for sale in result:
        if add_new_sale(sale):
            ctr += 1

    logger.info(f"Finished processing new sales. Added {ctr} new sales.")

    return result, ctr
