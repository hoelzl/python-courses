import pytest

from ..shopping_cart_entry import ShoppingCartEntry


def test_negative_number_of_items_not_allowed():
    with pytest.raises(ValueError):
        ShoppingCartEntry('123', 'Black Tea', 1.29, -1)


def test_number_of_items():
    unit = ShoppingCartEntry('123', 'Black Tea', 1.0, 1)
    assert unit.number_of_items == 1


def test_number_of_items_setter():
    unit = ShoppingCartEntry('123', 'Black Tea', 1.0, 1)
    unit.number_of_items = 5
    assert unit.number_of_items == 5


def test_total_price():
    unit = ShoppingCartEntry('123', 'Black Tea', 1.0, 3)
    assert unit.total_price == 3 * 1.0


def test_eq_for_equal_entries():
    entry1 = ShoppingCartEntry('123', 'Black Tea', 1.0, 3)
    entry2 = ShoppingCartEntry('123', 'Black Tea', 1.0, 3)
    assert entry1 == entry2


def test_str():
    assert str(ShoppingCartEntry('123', 'Black Tea', 1.0, 3)) \
           == "3 x Black Tea à 1.00, total 3.00"


def test_repr():
    assert repr(ShoppingCartEntry('123', 'Black Tea', 1.0, 3)) \
           == "ShoppingCartEntry('123', 'Black Tea', 1.0, 3)"
