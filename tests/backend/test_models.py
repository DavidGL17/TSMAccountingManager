from tsmaccountingmanager.backend.models import process_timestamp, process_price
from datetime import datetime


def test_process_timestamp():
    timestamp = 1642241261
    date = process_timestamp(timestamp)
    print(date)
    # remove the tzinfo because it is not the same on every machine
    date = date.replace(tzinfo=None)
    assert date == datetime(2022, 1, 15, 11, 7, 41)


def test_process_price():
    price = 100000
    gold, total = process_price(price, 2)
    assert gold == 10.0
    assert total == 20.0
