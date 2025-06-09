import pytest
import sys

sys.path.append(".")


def write_data():
    from play.db import Database
    db = Database()

    db.set_data("test", "value")
    assert db.get_data("test") == "value"
    db.set_data("test_nested", {})
    db.set_data("test_nested:sub", "value")
    assert db.get_data("test_nested:sub") == "value"


def check_data():
    from play.db import Database
    db = Database()

    assert db.get_data("test") == "value"
    assert db.get_data("test_nested:sub") == "value"


def cleanup():
    import os

    os.remove("database.json")


def test_db():
    write_data()
    check_data()


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want

    yield  # this is where the testing happens

    cleanup()


if __name__ == "__main__":
    test_db()
