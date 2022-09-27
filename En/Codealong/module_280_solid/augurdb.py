# %%
from dataclasses import dataclass, field
from typing import Any

# %%
Records = dict[str, dict[str, Any]]


# %%
class TransactionError(RuntimeError):
    pass


# %%
@dataclass
class AugurDatabase:
    records: Records = field(default_factory=dict)
    current_transaction: Records | None = None

    def start_transaction(self):
        """Start a new transaction.

        Raise a `TransactionError` if a transaction is already active.

        >>> db = AugurDatabase()
        >>> db.start_transaction()
        >>> db.start_transaction()
        Traceback (most recent call last):
        ...
        augurdb.TransactionError: Cannot start a nested transaction.
        """
        if self.current_transaction is None:
            self.current_transaction = {}
        else:
            raise TransactionError("Cannot start a nested transaction.")

    def commit_transaction(self):
        """Commit a transaction.

        Raise a `TransactionError` if no transaction is currently active.

        >>> db = AugurDatabase()
        >>> db.commit_transaction()
        Traceback (most recent call last):
        ...
        augurdb.TransactionError: No active transaction.

        >>> db = AugurDatabase()
        >>> db.start_transaction()
        >>> db.current_transaction
        {}
        >>> db.store_field("obj1", "field1", 1)
        >>> db.store_field("obj2", "field1", 2)
        >>> db.store_field("obj1", "field2", 3)
        >>> db.store_field("obj1", "field1", 4)
        >>> db.records
        {}
        >>> db.current_transaction
        {'obj1': {'field1': 4, 'field2': 3}, 'obj2': {'field1': 2}}
        >>> db.commit_transaction()
        >>> db.records
        {'obj1': {'field1': 4, 'field2': 3}, 'obj2': {'field1': 2}}
        >>> db.current_transaction is None
        True
        """
        if self.current_transaction is None:
            raise TransactionError("No active transaction.")
        else:
            for obj_id, new_values in self.current_transaction.items():
                old_values = self.records.setdefault(obj_id, {})
                old_values.update(new_values)
            self.current_transaction = None

    def rollback_transaction(self):
        """Roll back the current transaction.

        Raise a `TransactionError` if no transaction is currently active.

        >>> db = AugurDatabase()
        >>> db.rollback_transaction()
        Traceback (most recent call last):
        ...
        augurdb.TransactionError: No active transaction.

        >>> db = AugurDatabase()
        >>> db.start_transaction()
        >>> db.current_transaction
        {}
        >>> db.store_field("obj1", "field1", 1)
        >>> db.records
        {}
        >>> db.current_transaction
        {'obj1': {'field1': 1}}
        >>> db.rollback_transaction()
        >>> db.records
        {}
        >>> db.current_transaction is None
        True
        """
        if self.current_transaction is None:
            raise TransactionError("No active transaction.")
        else:
            self.current_transaction = None

    def store_field(self, obj_id, name, value):
        """Store the value for a field in the current transaction.

        Raise a `TransactionError` if no transaction is currently active.

        >>> db = AugurDatabase()
        >>> db.store_field("obj1", "field1", 1)
        Traceback (most recent call last):
        ...
        augurdb.TransactionError: No active transaction.

        >>> db = AugurDatabase()
        >>> db.start_transaction()
        >>> db.store_field("obj1", "field1", 1)
        >>> db.store_field("obj2", "field1", 2)
        >>> db.store_field("obj1", "field2", 3)
        >>> db.commit_transaction()
        >>> db.records
        {'obj1': {'field1': 1, 'field2': 3}, 'obj2': {'field1': 2}}
        """
        if self.current_transaction is None:
            raise TransactionError("No active transaction.")
        else:
            obj_record = self.current_transaction.setdefault(obj_id, {})
            obj_record[name] = value

# %%
