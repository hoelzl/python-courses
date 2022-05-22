class ShoppingCartEntry:
    def __init__(self, article_number, article_name, price_per_item,
                 number_of_items):
        self.article_number = article_number
        self.article_name = article_name
        self.price_per_item = float(price_per_item)
        self.number_of_items = int(number_of_items)

    @property
    def number_of_items(self):
        return self._number_of_items

    @number_of_items.setter
    def number_of_items(self, new_value):
        if new_value <= 0:
            raise ValueError("Number of items must be positive.")
        else:
            self._number_of_items = new_value

    @property
    def total_price(self):
        """Compute the total price of this shopping cart entry"""
        return self.price_per_item * self.number_of_items

    def __eq__(self, other):
        if isinstance(other, ShoppingCartEntry):
            return (self.article_number == other.article_number
                    and self.article_name == other.article_name
                    and self.price_per_item == other.price_per_item
                    and self.number_of_items == other.number_of_items)
        else:
            return False

    def __str__(self):
        return (f"{self.number_of_items} x "
                f"{self.article_name} à {self.price_per_item:.2f}, "
                f"total {self.total_price:.2f}")

    def __repr__(self):
        return (f"ShoppingCartEntry({self.article_number!r}, "
                f"{self.article_name!r}, {self.price_per_item!r}, "
                f"{self.number_of_items!r})")
