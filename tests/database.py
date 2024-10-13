import pytest


def write_data():
    from play.db import get_data, set_data

    set_data("test", "value")
    assert get_data("test") == "value"
    set_data("test_nested", {})
    set_data("test_nested:sub", "value")
    assert get_data("test_nested:sub") == "value"


def check_data():
    from play.db import get_data

    assert get_data("test") == "value"
    assert get_data("test_nested:sub") == "value"


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
