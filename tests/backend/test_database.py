from tsmaccountingmanager.backend.database import zodb


def test_database_init():
    # assert that the database is initialized
    assert "items" in zodb.dbroot["app_data"]
    assert "categories" in zodb.dbroot["app_data"]
    assert "purchases" in zodb.dbroot["app_data"]
    assert "sales" in zodb.dbroot["app_data"]
    assert zodb.dbroot["app_data"]["categories"]["default"].name == "Default"
