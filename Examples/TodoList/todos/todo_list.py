import pickle
from typing import List

from .todo_item import TodoItem


class TodoList:
    def __init__(self, items):
        self.items: List[TodoItem] = [TodoItem(**spec) for spec in items]

    def add(self, title, priority=1, is_completed=False):
        self.items.append(TodoItem(title, priority, is_completed))

    def mark_completed(self, title):
        for item in self.items:
            if item.title == title and not item.is_completed:
                item.is_completed = True
                break

    def delete(self, title):
        index_to_delete = -1
        for index, item in enumerate(self.items):
            if item.title == title:
                index_to_delete = index
                break
        if index_to_delete >= 0:
            del self.items[index_to_delete]

    def delete_all_completed(self):
        indices_to_delete = []
        # To keep PyCharm happy
        assert isinstance(self.items, list)
        for index, item in enumerate(self.items):
            if item.is_completed:
                indices_to_delete.append(index)
        import numpy as np
        self.items = np.delete(self.items, indices_to_delete).tolist()

    def save_to_file(self, file):
        pickle.dump(self, file)

    @staticmethod
    def load_from_file(file):
        try:
            return pickle.load(file)
        except (pickle.UnpicklingError, EOFError):
            return TodoList([])

    def __str__(self):
        from io import StringIO
        result = StringIO()
        print("Todo List:", file=result)
        for item in self.items:
            print(f"  {item!s}", file=result)
        return result.getvalue()

    def __repr__(self):
        return f"TodoList({self.items!r})"

    def __iter__(self):
        # return iter(self.items)
        return (i for i in self.items)
