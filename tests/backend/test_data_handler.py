from tsmaccountingmanager.backend.database import zodb, check_item_exists, delete_elements
from tsmaccountingmanager.backend.data_handler import process_expenses, process_sales
from tsmaccountingmanager.backend.models import Source
from general_utils import (
    test_data_expenses_path,
    test_data_sales_path,
    purchases_list,
    sales_list,
    full_data_expenses_path,
    full_data_sales_path,
)
import pandas as pd


def test_process_expenses():
    expensesDF = pd.read_csv(test_data_expenses_path)
    result = process_expenses(expensesDF)
    assert result == purchases_list
    # check that all items are in the database, and all purchases are in the database
    for expense in result:
        assert check_item_exists(expense.item)
        assert zodb.dbroot["app_data"]["purchases"].get(str(expense.id))

    # clean up
    delete_elements("items", [expense.item for expense in result])
    delete_elements("purchases", [expense.id for expense in result])


def test_process_sales():
    salesDF = pd.read_csv(test_data_sales_path)
    result = process_sales(salesDF)
    assert result == sales_list
    # check that all items are in the database
    for sale in result:
        assert check_item_exists(sale.item)
        assert zodb.dbroot["app_data"]["sales"].get(str(sale.id))

    # clean up
    delete_elements("items", [sale.item for sale in result])
    delete_elements("sales", [sale.id for sale in result])


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
    # check that all purchases are in the database
    for purchase in expenses:
        assert zodb.dbroot["app_data"]["purchases"].get(str(purchase.id))
    # check that all sales are in the database
    for sale in sales:
        assert zodb.dbroot["app_data"]["sales"].get(str(sale.id))
    # clean up
    delete_elements("items", [expense.item for expense in expenses])
    delete_elements("purchases", [expense.id for expense in expenses])
    delete_elements("items", [sale.item for sale in sales])
    delete_elements("sales", [sale.id for sale in sales])
