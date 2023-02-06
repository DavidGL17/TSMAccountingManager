from tsmaccountingmanager.backend.database import zodb, check_item_exists
from tsmaccountingmanager.backend.data_handler import process_expenses, process_sales, process_timestamp
from tsmaccountingmanager.backend.models import Sale, Purchase, Source
import transaction
import pandas as pd


sales_list = [
    Sale(
        item=109125,
        stackSize=500,
        quantity=500,
        price=2.8025,
        total=1401.25,
        time=process_timestamp(1642346545),
        source=Source.AUCTION,
    ),
    Sale(
        item=34055,
        stackSize=1,
        quantity=1,
        price=10.925,
        total=10.925,
        time=process_timestamp(1642346545),
        source=Source.AUCTION,
    ),
    Sale(
        item=9999,
        stackSize=1,
        quantity=1,
        price=570.494,
        total=570.494,
        time=process_timestamp(1642334948),
        source=Source.AUCTION,
    ),
    Sale(
        item=158867,
        stackSize=1,
        quantity=7,
        price=1.4392,
        total=1.4392,
        time=process_timestamp(1642074797),
        source=Source.VENDOR,
    ),
    Sale(
        item=176797,
        stackSize=1,
        quantity=1,
        price=45.2496,
        total=45.2496,
        time=process_timestamp(1642156040),
        source=Source.VENDOR,
    ),
    Sale(
        item=176391,
        stackSize=1,
        quantity=7,
        price=1.1949,
        total=1.1949,
        time=process_timestamp(1642074797),
        source=Source.VENDOR,
    ),
]
expenses_list = [
    Purchase(
        item=53010,
        stackSize=950,
        quantity=950,
        price=1.1372,
        total=1080.34,
        time=process_timestamp(1642191158),
        source=Source.AUCTION,
    ),
    Purchase(
        item=173033,
        stackSize=993,
        quantity=993,
        price=14.1309,
        total=14031.9837,
        time=process_timestamp(1641925080),
        source=Source.AUCTION,
    ),
    Purchase(
        item=179314,
        stackSize=498,
        quantity=498,
        price=14.5683,
        total=7255.013400000001,
        time=process_timestamp(1641925078),
        source=Source.AUCTION,
    ),
    Purchase(
        item=172056,
        stackSize=200,
        quantity=1000,
        price=0.4,
        total=80.0,
        time=process_timestamp(1641925230),
        source=Source.VENDOR,
    ),
    Purchase(
        item=172057,
        stackSize=200,
        quantity=800,
        price=0.3,
        total=60.0,
        time=process_timestamp(1641925223),
        source=Source.VENDOR,
    ),
    Purchase(
        item=4497,
        stackSize=1,
        quantity=3,
        price=1.9,
        total=1.9,
        time=process_timestamp(1641414852),
        source=Source.VENDOR,
    ),
]

test_data_expenses_path = "tests/data/test_data_expenses.csv"
test_data_sales_path = "tests/data/test_data_sales.csv"


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
