import pytest
import shutil
import os


@pytest.fixture(autouse=True)
def setup():
    # remove the data folder's content
    if os.path.exists("data"):
        shutil.rmtree("data")
