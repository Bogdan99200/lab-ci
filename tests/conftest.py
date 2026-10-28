import pytest

from shop.cart import Cart


@pytest.fixture
def cart() -> Cart:
    return Cart()


@pytest.fixture
def filled_cart() -> Cart:
    result = Cart()
    result.add("book", 200.0, 2)
    result.add("pen", 15.0, 4)
    return result
