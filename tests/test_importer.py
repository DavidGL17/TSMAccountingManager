from app.importer.importer import tmp
from app import __version__


def test_tmp():
    assert tmp() == 0


def test_version():

    assert __version__ == "0.1.0"
