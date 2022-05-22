import csv
import pickle
from collections.abc import Mapping
from io import StringIO
from pathlib import Path

from .shopping_cart_entry import ShoppingCartEntry


class ShoppingCart:
    def __init__(self, entry_specs):
        """Create a Shopping cart from entry specs.

        An entry spec is a dictionary with keys
        - article_number
        - article_name
        - price_per_item
        - number_of_items
        or a sequence with these four entries in the given order.
        All fields are required
        """
        self.entries = [
            (
                ShoppingCartEntry(**entry_spec)
                if isinstance(entry_spec, Mapping)
                else ShoppingCartEntry(*entry_spec)
            )
            for entry_spec in entry_specs
        ]

    @staticmethod
    def from_csv_path(path: Path):
        with path.open("r", encoding="utf-8") as file:
            return ShoppingCart.from_csv(file)

    @staticmethod
    def from_csv(file):
        """
        Constructor for Shopping carts

        Takes a CSV file where each line contains the following fields:
        - article number
        - article name
        - price per item
        - number of items
        in this order.
        Returns a shopping cart containing these entries
        """
        reader = csv.reader(file)
        return ShoppingCart(iter(reader))
        # Alternative:
        # entries = [{'article_number': art_nr,
        #             'article_name': name,
        #             'price_per_item': float(ppi),
        #             'number_of_items': int(num)}
        #            for art_nr, name, ppi, num in reader]
        # return ShoppingCart(entries)

    @property
    def total_price(self):
        """Compute the total price of all items in the cart"""
        result = 0.0
        for entry in self.entries:
            result += entry.total_price
        return result

    def add(self, spec):
        """Add en entry for the supplied spec to the shopping cart"""
        self.entries.append(ShoppingCartEntry(**spec))

    def delete(self, spec):
        """Delete the first entry that matches spec from the shopping cart"""
        try:
            index = self.entries.index(ShoppingCartEntry(**spec))
            del self.entries[index]
        except ValueError:
            pass

    def save_to_path(self, path: Path):
        with path.open("wb") as file:
            self.save_to_file(file)

    def save_to_file(self, file):
        pickle.dump(self, file)

    @staticmethod
    def load_from_path(path: Path):
        with path.open("rb") as file:
            return ShoppingCart.load_from_file(file)

    @staticmethod
    def load_from_file(file):
        try:
            return pickle.load(file)
        except (pickle.UnpicklingError, EOFError):
            print(f"Could not load {file}.")
            return ShoppingCart([])

    def __str__(self):
        stream = StringIO()
        print(
            f"Shopping cart with {len(self.entries)} "
            f"{'entry' if len(self.entries) == 1 else 'entries'}:",
            file=stream,
        )
        for item in self.entries:
            print(f"  {item!s}", file=stream)
        print(f"Total: {self.total_price:.2f}", file=stream)
        return stream.getvalue()

    def __repr__(self):
        return f"ShoppingCart({self.entries!r})"
