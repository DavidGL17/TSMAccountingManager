from tsmaccountingmanager.backend.database import zodb, check_item_exists
from tsmaccountingmanager.backend.data_handler import process_expenses, process_sales, insert_purchases, insert_sales
from tsmaccountingmanager.backend.models import Source
from general_utils import (
    test_data_expenses_path,
    test_data_sales_path,
    expenses_list,
    sales_list,
    full_data_expenses_path,
    full_data_sales_path,
)
import transaction
import pandas as pd


def test_process_expenses():
    expensesDF = pd.read_csv(test_data_expenses_path)
    result = process_expenses(expensesDF)
    assert result == expenses_list
    # check that all items are in the database
    for expense in result:
        assert check_item_exists(expense.item)

    # clean up
    for expense in result:
        zodb.dbroot["app_data"]["items"].pop(str(expense.item))
    transaction.commit()


def test_process_sales():
    salesDF = pd.read_csv(test_data_sales_path)
    result = process_sales(salesDF)
    assert result == sales_list
    # check that all items are in the database
    for sale in result:
        assert check_item_exists(sale.item)

    # clean up
    for sale in result:
        zodb.dbroot["app_data"]["items"].pop(str(sale.item))
    transaction.commit()


def test_insert_purchases():
    insert_purchases(expenses_list)
    # check that all purchases are in the database
    for purchase in expenses_list:
        assert zodb.dbroot["app_data"]["purchases"].get(str(purchase.id))
    # clean up
    for purchase in expenses_list:
        zodb.dbroot["app_data"]["purchases"].pop(str(purchase.id))
    transaction.commit()


def test_insert_sales():
    insert_sales(sales_list)
    # check that all sales are in the database
    for sale in sales_list:
        assert zodb.dbroot["app_data"]["sales"].get(str(sale.id))
    # clean up
    for sale in sales_list:
        zodb.dbroot["app_data"]["sales"].pop(str(sale.id))
    transaction.commit()


def test_full_insert():
    expensesDF = pd.read_csv(full_data_expenses_path)
    salesDF = pd.read_csv(full_data_sales_path)
    expenses = process_expenses(expensesDF)
    sales = process_sales(salesDF)

    # make sure all the sales/expenses in the lists are acceptable
    for expense in expenses:
        assert expense.source != Source.VENDOR
    for sale in sales:
        assert sale.source != Source.VENDOR

    # inspect all items in the database and make sure they are acceptable
    for item in zodb.dbroot["app_data"]["items"].values():
        assert item.name != "?"

    insert_purchases(expenses)
    insert_sales(sales)
    # check that all purchases are in the database
    for purchase in expenses:
        assert zodb.dbroot["app_data"]["purchases"].get(str(purchase.id))
    # check that all sales are in the database
    for sale in sales:
        assert zodb.dbroot["app_data"]["sales"].get(str(sale.id))
    # clean up
    for purchase in expenses:
        zodb.dbroot["app_data"]["purchases"].pop(str(purchase.id))
    for sale in sales:
        zodb.dbroot["app_data"]["sales"].pop(str(sale.id))
    transaction.commit()
