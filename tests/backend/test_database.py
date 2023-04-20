from tsmaccountingmanager.backend.database import (
    SingletonZODB,
    delete_element,
    delete_elements,
    add_new_item,
    check_item_exists,
    add_new_purchase,
    add_new_sale,
    add_new_category,
    get_purchases,
    get_purchases_by_time,
    get_purchases_by_item,
    get_purchases_by_category,
    get_sales,
    get_sales_by_time,
    get_sales_by_item,
    get_sales_by_category,
    get_items,
    get_item_by_id,
    get_items_by_category,
    get_categories,
    get_category_by_id,
)
from tsmaccountingmanager.backend.data_handler import (
    process_expenses,
    process_sales,
    process_timestamp,
)
from tsmaccountingmanager.backend.models import Category, Purchase, Sale, Source
from general_utils import test_data_expenses_path, test_data_sales_path, sales_list, purchases_list
import pandas as pd
from datetime import datetime

###
# Database Init Tests
###


def test_database_init():
    # assert that the database is initialized
    with SingletonZODB as zodb:
        assert "items" in zodb.dbroot["app_data"]
        assert "categories" in zodb.dbroot["app_data"]
        assert "purchases" in zodb.dbroot["app_data"]
        assert "sales" in zodb.dbroot["app_data"]
        assert "0" in zodb.dbroot["app_data"]["categories"]
        assert zodb.dbroot["app_data"]["categories"]["0"].name == "Default"


###
# Database insertion tests
###


def test_check_item_exists():
    item_id = 123456
    assert not check_item_exists(item_id)
    with SingletonZODB as zodb:
        assert not zodb.dbroot["app_data"]["items"].get(str(item_id))
        assert zodb.dbroot["app_data"]["items"].get(str(item_id)) is None
        zodb.dbroot["app_data"]["items"][str(item_id)] = "Test Item"
    assert check_item_exists(item_id)
    with SingletonZODB as zodb:
        assert zodb.dbroot["app_data"]["items"].get(str(item_id))
        assert zodb.dbroot["app_data"]["items"][str(item_id)] == "Test Item"
    # cleanup
    delete_element("items", item_id)


def test_add_new_item():
    item_id = 123456
    item_name = "Test Item"
    with SingletonZODB as zodb:
        assert not zodb.dbroot["app_data"]["items"].get(str(item_id))
        assert zodb.dbroot["app_data"]["items"].get(str(item_id)) is None
    assert add_new_item(item_id, item_name)
    with SingletonZODB as zodb:
        assert zodb.dbroot["app_data"]["items"].get(str(item_id))
        assert zodb.dbroot["app_data"]["items"][str(item_id)].name == item_name
    # cleanup
    delete_element("items", item_id)


def test_add_new_purchase():
    for purchase in purchases_list:
        assert add_new_purchase(purchase)
        # cleanup
        delete_element("items", purchase.item)
        delete_element("purchases", purchase.id)


def test_add_new_sale():
    for sale in sales_list:
        assert add_new_sale(sale)
        # cleanup
        delete_element("items", sale.item)
        delete_element("sales", sale.id)


def test_add_new_category():
    newCategory = Category(name="Test Category")
    # check that the category doesn't exist
    with SingletonZODB as zodb:
        assert not zodb.dbroot["app_data"]["categories"].get(str(newCategory.id))

    # add the category
    assert add_new_category(newCategory)

    # check that the category exists
    with SingletonZODB as zodb:
        assert zodb.dbroot["app_data"]["categories"].get(str(newCategory.id))
        assert zodb.dbroot["app_data"]["categories"][str(newCategory.id)].name == "Test Category"

    # assert we can't add the same category twice
    assert not add_new_category(newCategory)

    # cleanup
    delete_element("categories", newCategory.id)


###
# Test Getters
###


def test_get_purchases():
    purchases, ctr = process_expenses(pd.read_csv(test_data_expenses_path))
    assert len(get_purchases()) == len(purchases)
    # make sur the purchases are the same
    for purchase in get_purchases():
        assert purchase in purchases
    # cleanup
    delete_elements("purchases", [purchase.id for purchase in purchases])
    delete_elements("items", [purchase.item for purchase in purchases])


def test_get_purchases_by_time():
    purchases, ctr = process_expenses(pd.read_csv(test_data_expenses_path))
    dates = [
        (process_timestamp(1641925077.0), process_timestamp(1641925081.0)),
        (process_timestamp(1642191157.0), process_timestamp(1642191159.0)),
    ]
    first_result = get_purchases_by_time(dates[0][0], dates[0][1])
    second_result = get_purchases_by_time(dates[1][0], dates[1][1])
    assert len(first_result) == 2
    assert len(second_result) == 1
    assert first_result[0] == purchases[0]
    assert first_result[1] == purchases[1]
    assert second_result[0] == purchases[2]
    # cleanup
    delete_elements("purchases", [purchase.id for purchase in purchases])
    delete_elements("items", [purchase.item for purchase in purchases])


def test_get_purchases_by_item():
    purchases, ctr = process_expenses(pd.read_csv(test_data_expenses_path))
    item_ids = [purchase.item for purchase in purchases]
    for item_id in item_ids:
        assert get_purchases_by_item(item_id) == [purchase for purchase in purchases if purchase.item == item_id]
    # cleanup
    delete_elements("purchases", [purchase.id for purchase in purchases])
    delete_elements("items", [purchase.item for purchase in purchases])


def test_get_purchases_by_category():
    purchases, ctr = process_expenses(pd.read_csv(test_data_expenses_path))
    for purchase in purchases:
        add_new_purchase(purchase)
    assert get_purchases_by_category(0) == purchases
    # cleanup
    delete_elements("purchases", [purchase.id for purchase in purchases])
    delete_elements("items", [purchase.item for purchase in purchases])


def test_get_sales():
    sales, ctr = process_sales(pd.read_csv(test_data_sales_path))
    assert len(get_sales()) == len(sales)
    # make sur the sales are the same
    for sale in get_sales():
        assert sale in sales
    # cleanup
    delete_elements("sales", [sale.id for sale in sales])
    delete_elements("items", [sale.item for sale in sales])


def test_get_sales_by_time():
    sales, ctr = process_sales(pd.read_csv(test_data_sales_path))
    dates = [
        (process_timestamp(1642069200.0), process_timestamp(1642069202.0)),
        (process_timestamp(1642334947.0), process_timestamp(1642346546.0)),
    ]
    first_result = get_sales_by_time(dates[0][0], dates[0][1])
    second_result = get_sales_by_time(dates[1][0], dates[1][1])
    assert len(first_result) == 1
    assert len(second_result) == 2
    assert first_result[0] == sales[0]
    assert second_result[0] == sales[1]
    assert second_result[1] == sales[2]
    # cleanup
    delete_elements("sales", [sale.id for sale in sales])


def test_get_sales_by_item():
    sales, ctr = process_sales(pd.read_csv(test_data_sales_path))
    item_ids = [sale.item for sale in sales]
    for item_id in item_ids:
        assert get_sales_by_item(item_id) == [sale for sale in sales if sale.item == item_id]
    # cleanup
    delete_elements("sales", [sale.id for sale in sales])
    delete_elements("items", [sale.item for sale in sales])


def test_get_sales_by_category():
    sales, ctr = process_sales(pd.read_csv(test_data_sales_path))
    for sale in sales:
        add_new_sale(sale)
    assert get_sales_by_category(0) == sales
    # cleanup
    delete_elements("sales", [sale.id for sale in sales])
    delete_elements("items", [sale.item for sale in sales])


def test_get_items():
    sales, ctr = process_sales(pd.read_csv(test_data_sales_path))
    purchases, ctr = process_expenses(pd.read_csv(test_data_expenses_path))
    items = [sale.item for sale in sales] + [purchase.item for purchase in purchases]
    result = get_items()
    assert len(result) == len(items)
    # make sur the items are the same
    for item in result:
        assert item.id in items
    # cleanup
    delete_elements("items", [item for item in items])
    delete_elements("sales", [sale.id for sale in sales])
    delete_elements("purchases", [purchase.id for purchase in purchases])


def test_get_item_by_id():
    sales, ctr = process_sales(pd.read_csv(test_data_sales_path))
    purchases, ctr = process_expenses(pd.read_csv(test_data_expenses_path))
    items = [sale.item for sale in sales] + [purchase.item for purchase in purchases]
    for item in items:
        res = get_item_by_id(item)
        assert res.id == item

    # cleanup
    delete_elements("items", [item for item in items])
    delete_elements("sales", [sale.id for sale in sales])
    delete_elements("purchases", [purchase.id for purchase in purchases])


def test_get_items_by_category():
    sales, ctr = process_sales(pd.read_csv(test_data_sales_path))
    purchases, ctr = process_expenses(pd.read_csv(test_data_expenses_path))
    items = [sale.item for sale in sales] + [purchase.item for purchase in purchases]
    result = get_items_by_category(0)
    assert len(result) == len(items)

    # cleanup
    delete_elements("items", [item for item in items])
    delete_elements("sales", [sale.id for sale in sales])
    delete_elements("purchases", [purchase.id for purchase in purchases])


def test_get_categories():
    result = get_categories()
    assert len(result) == 1
    assert result[0].id == 0
    assert result[0].name == "Default"

    newCategory = Category("Test")
    add_new_category(newCategory)
    categories = result + [newCategory]
    result = get_categories()
    assert result == categories

    # cleanup
    delete_element("categories", newCategory.id)


def test_get_category_by_id():
    newCategory = Category("Test")
    add_new_category(newCategory)
    result = get_category_by_id(newCategory.id)
    assert result == newCategory

    result = get_category_by_id(0)
    assert result.id == 0
    assert result.name == "Default"

    # cleanup
    delete_element("categories", newCategory.id)


###
# Delete functions
###


def test_delete_element():
    newCategory = Category("Test")
    add_new_category(newCategory)
    delete_element("categories", newCategory.id)
    result = get_category_by_id(newCategory.id)
    assert result is None

    add_new_item(0, "Test")
    delete_element("items", 0)
    result = get_item_by_id(0)
    assert result is None

    newPurchase = Purchase(0, 0, 0, 0, 0, datetime.now(), Source.AUCTION)
    add_new_purchase(newPurchase)
    delete_element("purchases", newPurchase.id)
    with SingletonZODB() as zodb:
        assert zodb.dbroot["app_data"]["purchases"].get(str(newPurchase.id)) is None

    newSale = Sale(0, 0, 0, 0, 0, datetime.now(), Source.AUCTION)
    add_new_sale(newSale)
    delete_element("sales", newSale.id)
    with SingletonZODB() as zodb:
        assert zodb.dbroot["app_data"]["sales"].get(str(newSale.id)) is None


def test_delete_elements():
    newCategories = [Category("Test"), Category("Test2")]
    add_new_category(newCategories[0])
    add_new_category(newCategories[1])
    delete_elements("categories", [newCategories[0].id, newCategories[1].id])
    result = get_categories()
    assert len(result) == 1
    assert result[0].id == 0
    assert result[0].name == "Default"

    sales, ctr = process_sales(pd.read_csv(test_data_sales_path))
    purchases, ctr = process_expenses(pd.read_csv(test_data_expenses_path))
    items = [sale.item for sale in sales] + [purchase.item for purchase in purchases]

    delete_elements("items", items)
    result = get_items()
    assert len(result) == 0

    delete_elements("sales", [sale.id for sale in sales])
    result = get_sales()
    assert len(result) == 0

    delete_elements("purchases", [purchase.id for purchase in purchases])
    result = get_purchases()
    assert len(result) == 0
