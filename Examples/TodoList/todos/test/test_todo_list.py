from todos.todo_item import TodoItem
from todos.todo_list import TodoList
from io import BytesIO


def test_constructor():
    unit = TodoList([{'title': 'Foo'},
                     {'title': 'Bar', 'priority': 10},
                     {'title': 'Baz', 'is_completed': True}])
    assert unit.items == [
        TodoItem('Foo'),
        TodoItem('Bar', priority=10),
        TodoItem('Baz', is_completed=True)
    ]


def test_add_with_defaults():
    unit = TodoList([{'title': 'Foo'}])
    unit.add('Bar')

    assert unit.items == [TodoItem('Foo'), TodoItem('Bar')]


def test_add_with_explicit_values():
    unit = TodoList([{'title': 'Foo'}])
    unit.add('Bar', 10, True)

    assert unit.items == [TodoItem('Foo'), TodoItem('Bar', 10, True)]


def test_mark_completed():
    unit = TodoList([{'title': 'Foo'}, {'title': 'Bar', 'is_completed': True},
                     {'title': 'Baz'}, {'title': 'Bar'},
                     {'title': 'Quux'}, {'title': 'Bar'}])
    unit.mark_completed('Bar')

    assert unit.items == [TodoItem('Foo'), TodoItem('Bar', is_completed=True),
                          TodoItem('Baz'), TodoItem('Bar', is_completed=True),
                          TodoItem('Quux'), TodoItem('Bar')]


def test_delete_with_matching_item():
    unit = TodoList([{'title': 'Foo'}, {'title': 'Bar'},
                     {'title': 'Baz'}, {'title': 'Bar', 'priority': 2},
                     {'title': 'Quux'}])
    unit.delete('Bar')

    assert unit.items == [TodoItem('Foo'), TodoItem('Baz'),
                          TodoItem('Bar', 2), TodoItem('Quux')]


def test_delete_without_matching_item():
    unit = TodoList([{'title': 'Foo'}, {'title': 'Bar'},
                     {'title': 'Baz'}])
    unit.delete('Quux')

    assert unit.items == [TodoItem('Foo'), TodoItem('Bar'), TodoItem('Baz')]


def test_delete_all_completed():
    # All odd items are completed
    unit = TodoList([{'title': f"Item {i}", 'is_completed': i % 2 == 1}
                     for i in range(0, 10)])
    unit.delete_all_completed()

    # Result should only contain the even items
    assert unit.items == [TodoItem(f"Item {i}")
                          for i in range(0, 10, 2)]


def test_save_to_and_load_from_file():
    buffer = BytesIO()
    unit = TodoList([{'title': 'Foo'}, {'title': 'Bar', 'is_completed': True},
                     {'title': 'Baz'}, {'title': 'Bar', 'priority': 2},
                     {'title': 'Quux', 'is_completed': True}])
    unit.save_to_file(buffer)
    buffer.seek(0)

    restored_unit = TodoList.load_from_file(buffer)
    assert isinstance(restored_unit, TodoList)
    assert restored_unit is not unit
    assert restored_unit.items is not unit.items
    assert restored_unit.items == unit.items


def test_load_from_empty_file():
    buffer = BytesIO()
    unit = TodoList.load_from_file(buffer)

    assert isinstance(unit, TodoList)
    assert unit.items == []


def test_str():
    unit = TodoList([{'title': 'Foo'}, {'title': 'Bar', 'is_completed': True},
                     {'title': 'Baz'}, {'title': 'Bar', 'priority': 2},
                     {'title': 'Quux', 'is_completed': True}])
    assert str(unit) == """Todo List:
  Foo, priority 1
  Bar, priority 1, done
  Baz, priority 1
  Bar, priority 2
  Quux, priority 1, done
"""


def test_repr():
    unit = TodoList([{'title': 'Foo'}])
    assert repr(unit) == "TodoList([TodoItem('Foo', 1, False)])"


def test_iter():
    item_specs = [{'title': 'Foo'}, {'title': 'Bar', 'is_completed': True},
                  {'title': 'Baz'}, {'title': 'Bar', 'priority': 2},
                  {'title': 'Quux', 'is_completed': True}]
    unit = TodoList(item_specs)

    for index, item in enumerate(unit):
        assert TodoItem(**item_specs[index]) == item
