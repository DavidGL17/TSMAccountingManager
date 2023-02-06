from tsmaccountingmanager.backend.database import zodb, add_new_item, check_item_exists, add_new_purchase, add_new_sale
from tsmaccountingmanager.backend.data_handler import process_expenses, process_sales
import transaction
from general_utils import test_data_expenses_path, test_data_sales_path
import pandas as pd


def test_database_init():
    # assert that the database is initialized
    assert "items" in zodb.dbroot["app_data"]
    assert "categories" in zodb.dbroot["app_data"]
    assert "purchases" in zodb.dbroot["app_data"]
    assert "sales" in zodb.dbroot["app_data"]
    assert "0" in zodb.dbroot["app_data"]["categories"]
    assert zodb.dbroot["app_data"]["categories"]["0"].name == "Default"


def test_check_item_exists():
    item_id = 123456
    assert not check_item_exists(item_id)
    assert not zodb.dbroot["app_data"]["items"].get(str(item_id))
    assert zodb.dbroot["app_data"]["items"].get(str(item_id)) is None
    zodb.dbroot["app_data"]["items"][str(item_id)] = "Test Item"
    assert check_item_exists(item_id)
    assert zodb.dbroot["app_data"]["items"].get(str(item_id))
    assert zodb.dbroot["app_data"]["items"][str(item_id)] == "Test Item"
    # cleanup
    del zodb.dbroot["app_data"]["items"][str(item_id)]
    transaction.commit()


def test_add_new_item():
    item_id = 123456
    item_name = "Test Item"
    assert not zodb.dbroot["app_data"]["items"].get(str(item_id))
    assert zodb.dbroot["app_data"]["items"].get(str(item_id)) is None
    assert add_new_item(item_id, item_name)
    assert zodb.dbroot["app_data"]["items"].get(str(item_id))
    assert zodb.dbroot["app_data"]["items"][str(item_id)].name == item_name
    # cleanup
    del zodb.dbroot["app_data"]["items"][str(item_id)]
    transaction.commit()


def test_add_new_purchase():
    expensesDF = pd.read_csv(test_data_expenses_path)
    purchases = process_expenses(expensesDF)
    for purchase in purchases:
        assert add_new_purchase(purchase)
        # cleanup
        zodb.dbroot["app_data"]["items"].pop(str(purchase.item))
        zodb.dbroot["app_data"]["purchases"].pop(str(purchase.id))
        transaction.commit()


def test_add_new_sale():
    salesDF = pd.read_csv(test_data_sales_path)
    sales = process_sales(salesDF)
    for sale in sales:
        assert add_new_sale(sale)
        # cleanup
        zodb.dbroot["app_data"]["items"].pop(str(sale.item))
        zodb.dbroot["app_data"]["sales"].pop(str(sale.id))
        transaction.commit()
