from tsmaccountingmanager.backend.models import (
    process_timestamp,
    process_price,
    extract_item_id,
    get_correct_source,
    Source,
    Sale,
)
from datetime import datetime


def test_process_timestamp():
    timestamp = 1642241261
    date = process_timestamp(timestamp)
    print(date)
    # remove the tzinfo because it is not the same on every machine
    date = date.replace(tzinfo=None)
    assert date == datetime(2022, 1, 15, 11, 7, 41)


def test_process_price():
    # check standard value
    price = 100000
    gold, total = process_price(price, 2)
    assert gold == 10.0
    assert total == 20.0

    # check with a price = 0
    price = 0
    gold, total = process_price(price, 2)
    assert gold == 0.0
    assert total == 0.0

    # check with a quantity = 0
    price = 100000
    gold, total = process_price(price, 0)
    assert gold == 10.0
    assert total == 0.0


def test_extract_item_id():
    items = [
        ("i:109125", 109125),
        ("i:34055", 34055),
        ("i:9999", 9999),
        ("i:158867", 158867),
        ("i:176797", 176797),
        ("i:176391", 176391),
        ("i:176797::3:1683:6652:6908:1:9:60", 176797),
    ]
    for itemString, id in items:
        assert extract_item_id(itemString) == id


def test_get_correct_source():
    assert get_correct_source("Auction") == Source.AUCTION
    assert get_correct_source("Vendor") == Source.VENDOR
    try:
        get_correct_source("Invalid")
        assert False
    except ValueError:
        assert True
