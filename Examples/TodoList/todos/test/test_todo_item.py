from ..todo_item import TodoItem


def test_default_args():
    unit = TodoItem('FooBar')

    assert unit.title == 'FooBar'
    assert unit.priority == 1
    assert unit.is_completed is False


def test_provided_args():
    unit = TodoItem('Quux', 2, True)

    assert unit.title == 'Quux'
    assert unit.priority == 2
    assert unit.is_completed is True


def test_str_for_non_completed_item():
    unit = TodoItem('Foo')
    assert str(unit) == "Foo, priority 1"


def test_str_for_completed_item():
    unit = TodoItem('Bar', 3, True)
    assert str(unit) == "Bar, priority 3, done"


def test_repr():
    unit = TodoItem('Foo')
    assert repr(unit) == "TodoItem('Foo', 1, False)"


def test_eq_for_identical_items():
    unit = TodoItem('Item')
    assert unit == unit


def test_eq_for_equal_items():
    item1 = TodoItem('Foo')
    item2 = TodoItem('Foo')
    assert item1 is not item2
    assert item1 == item2


def test_eq_for_different_title():
    item1 = TodoItem('Foo')
    item2 = TodoItem('Bar')
    assert item1 != item2


def test_eq_for_different_priority():
    item1 = TodoItem('Foo', priority=2)
    item2 = TodoItem('Foo', priority=5)
    assert item1 != item2


def test_eq_for_different_is_completed():
    item1 = TodoItem('Foo', is_completed=True)
    item2 = TodoItem('Foo', is_completed=False)
    assert item1 != item2
