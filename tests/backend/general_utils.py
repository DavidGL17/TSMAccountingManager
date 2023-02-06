"""General utility variables used in tests."""
from tsmaccountingmanager.backend.data_handler import process_timestamp
from tsmaccountingmanager.backend.models import Sale, Purchase, Source

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
]

test_data_expenses_path = "tests/data/test_data_expenses.csv"
test_data_sales_path = "tests/data/test_data_sales.csv"
full_data_expenses_path = "tests/data/full_data_expenses.csv"
full_data_sales_path = "tests/data/full_data_sales.csv"
