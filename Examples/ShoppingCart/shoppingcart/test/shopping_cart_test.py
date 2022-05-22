from io import StringIO, BytesIO

from ..shopping_cart import ShoppingCart
from ..shopping_cart_entry import ShoppingCartEntry


def create_breakfast_shopping_cart():
    return ShoppingCart([
        {'article_number': '123',
         'article_name': 'Black Tea',
         'price_per_item': 1.29,
         'number_of_items': 3},
        {'article_number': '010',
         'article_name': 'Oatmeal',
         'price_per_item': 2.19,
         'number_of_items': 1}
    ])


def test_construction_from_dict_specs():
    unit = create_breakfast_shopping_cart()
    assert unit.entries == [ShoppingCartEntry('123', 'Black Tea', 1.29, 3),
                            ShoppingCartEntry('010', 'Oatmeal', '2.19', '1')]


def test_construction_from_tuple_specs():
    unit = ShoppingCart([('123', 'Black Tea', 1.29, 3),
                         ('010', 'Oatmeal', '2.19', '1')])
    assert unit.entries == [ShoppingCartEntry('123', 'Black Tea', 1.29, 3),
                            ShoppingCartEntry('010', 'Oatmeal', 2.19, 1)]


def test_from_csv():
    csv_contents = "123,Black Tea,1.29,3\n010,Oatmeal,2.19,1"
    buffer = StringIO(csv_contents)

    unit = ShoppingCart.from_csv(buffer)

    assert isinstance(unit, ShoppingCart)
    assert unit.entries == [ShoppingCartEntry('123', 'Black Tea', 1.29, 3),
                            ShoppingCartEntry('010', 'Oatmeal', 2.19, 1)]


def test_total_price():
    unit = create_breakfast_shopping_cart()
    assert unit.total_price == 3 * 1.29 + 1 * 2.19


def test_add():
    unit = ShoppingCart([{'article_number': '123',
                          'article_name': 'Black Tea',
                          'price_per_item': 1.29,
                          'number_of_items': 3}])
    unit.add({'article_number': '010',
              'article_name': 'Oatmeal',
              'price_per_item': 2.19,
              'number_of_items': 1})
    assert unit.entries == [ShoppingCartEntry('123', 'Black Tea', 1.29, 3),
                            ShoppingCartEntry('010', 'Oatmeal', 2.19, 1)]


def test_delete_when_matching_item():
    unit = create_breakfast_shopping_cart()
    unit.delete({'article_number': '010',
                 'article_name': 'Oatmeal',
                 'price_per_item': 2.19,
                 'number_of_items': 1})
    assert unit.entries == [ShoppingCartEntry('123', 'Black Tea', 1.29, 3)]


def test_delete_when_no_matching_item():
    unit = create_breakfast_shopping_cart()
    unit.delete({'article_number': '017',
                 'article_name': 'Cornbread',
                 'price_per_item': 1.99,
                 'number_of_items': 2})
    assert unit.entries == [ShoppingCartEntry('123', 'Black Tea', 1.29, 3),
                            ShoppingCartEntry('010', 'Oatmeal', 2.19, 1)]


def test_save_to_and_load_from_file():
    buffer = BytesIO()
    unit = create_breakfast_shopping_cart()
    unit.save_to_file(buffer)
    buffer.seek(0)

    restored_unit = ShoppingCart.load_from_file(buffer)
    assert isinstance(restored_unit, ShoppingCart)
    assert restored_unit is not unit
    assert restored_unit.entries is not unit.entries
    assert restored_unit.entries == unit.entries


def test_load_from_empty_file():
    buffer = BytesIO()
    unit = ShoppingCart.load_from_file(buffer)

    assert isinstance(unit, ShoppingCart)
    assert unit.entries == []


def test_str():
    unit = create_breakfast_shopping_cart()
    assert str(unit) == ("Shopping cart with 2 entries:\n"
                         "  3 x Black Tea à 1.29, total 3.87\n"
                         "  1 x Oatmeal à 2.19, total 2.19\n"
                         "Total: 6.06\n")


def test_repr():
    unit = create_breakfast_shopping_cart()
    assert repr(unit) == ("ShoppingCart(["
                          "ShoppingCartEntry('123', 'Black Tea', 1.29, 3), "
                          "ShoppingCartEntry('010', 'Oatmeal', 2.19, 1)])")
