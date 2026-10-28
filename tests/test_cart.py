from unittest.mock import Mock

import pytest

from shop.cart import Cart, Item


def test_empty_cart_count(cart: Cart) -> None:
    assert cart.items_count() == 0


def test_add_one_item(cart: Cart) -> None:
    cart.add("book", 200.0)
    assert cart.items_count() == 1


def test_add_multiple_quantity(cart: Cart) -> None:
    cart.add("book", 200.0, 3)
    assert cart.items_count() == 3


def test_add_same_name_increases_quantity(cart: Cart) -> None:
    cart.add("book", 200.0, 2)
    cart.add("book", 200.0, 3)
    assert cart.items_count() == 5


def test_same_name_keeps_original_price(cart: Cart) -> None:
    cart.add("book", 200.0, 1)
    cart.add("book", 300.0, 1)
    assert cart.total() == 400.0


@pytest.mark.parametrize(
    ("price", "qty", "expected"),
    [
        (0.0, 1, 0.0),
        (100.0, 1, 100.0),
        (25.5, 2, 51.0),
        (10.0, 0 + 1, 10.0),
    ],
)
def test_total_values(cart: Cart, price: float, qty: int, expected: float) -> None:
    cart.add("item", price, qty)
    assert cart.total() == pytest.approx(expected)


@pytest.mark.parametrize(
    ("discount", "expected"),
    [
        (0, 400.0),
        (10, 360.0),
        (50, 200.0),
        (100, 0.0),
    ],
)
def test_discounts(cart: Cart, discount: float, expected: float) -> None:
    cart.add("book", 200.0, 2)
    assert cart.total(discount) == pytest.approx(expected)


def test_negative_price_raises(cart: Cart) -> None:
    with pytest.raises(ValueError, match="price"):
        cart.add("book", -1.0)


@pytest.mark.parametrize("qty", [0, -1])
def test_invalid_quantity_raises(cart: Cart, qty: int) -> None:
    with pytest.raises(ValueError, match="qty"):
        cart.add("book", 10.0, qty)


@pytest.mark.parametrize("discount", [-1, 101, 150])
def test_invalid_discount_raises(cart: Cart, discount: float) -> None:
    with pytest.raises(ValueError, match="discount_percent"):
        cart.total(discount)


def test_remove_item(cart: Cart) -> None:
    cart.add("book", 200.0)
    cart.remove("book")
    assert cart.items_count() == 0


def test_remove_missing_item_raises(cart: Cart) -> None:
    with pytest.raises(KeyError):
        cart.remove("missing")


def test_total_in_uses_mock(cart: Cart) -> None:
    cart.add("book", 400.0)
    rates = Mock()
    rates.get_rate.return_value = 40.0

    assert cart.total_in("USD", rates) == 10.0
    rates.get_rate.assert_called_once_with("USD")


@pytest.mark.parametrize("rate", [0.0, -1.0])
def test_invalid_rate_raises(cart: Cart, rate: float) -> None:
    rates = Mock()
    rates.get_rate.return_value = rate

    with pytest.raises(ValueError, match="rate"):
        cart.total_in("USD", rates)


def test_filled_cart_fixture(filled_cart: Cart) -> None:
    assert filled_cart.items_count() == 6
    assert filled_cart.total() == 460.0


def test_most_expensive_empty_cart(cart: Cart) -> None:
    assert cart.most_expensive() is None


def test_most_expensive_returns_highest_unit_price(cart: Cart) -> None:
    cart.add("book", 200.0)
    cart.add("pen", 15.0)
    result = cart.most_expensive()
    assert result == Item(name="book", price=200.0, qty=1)


def test_most_expensive_does_not_use_total_quantity(cart: Cart) -> None:
    cart.add("cheap", 10.0, 100)
    cart.add("expensive", 50.0, 1)
    result = cart.most_expensive()
    assert result is not None
    assert result.name == "expensive"

git add tests/test_cart.py