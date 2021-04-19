"""This module provides a Day class.

The Day consists of a list of transactions that occurred during the day and
a list of positions at the end of the day.

"""

import copy
from typing import Dict, Iterator, List

from .transaction import Transaction


class Day:
    """Class representing a day's worth of transactions.

    The class contains a list of transactions that occurred during the day.
    It also stores the positions at the end of the day.

    """

    _positions: Dict[str, float]
    _transactions: List[Transaction]

    def __init__(self):
        self._positions = {}
        self._transactions = []

    def add_position(self, symbol: str, quantity: float):
        """Add the specified position.

        This will replace the position for the specified symbol if it was
        already present.

        Args:
            symbol (str): Unique identifier symbol
            quantity (float): The number of shares for the specified symbol
        """
        self._positions[symbol] = quantity

    def add_transaction(self, transaction: Transaction):
        """Add the specified transaction to the Day.

        Args:
            transaction (Transaction): A Transaction object for the Day
        """
        self._transactions.append(transaction)

    def get_positions(self) -> Dict[str, float]:
        """Returns a dictionary representation of the positions.

        The return value can be modified without impacting the positions
        associated with the Day.

        Returns:
            Dict[str, float]: A dictionary mapping the symbol to the quantity
                of that symbol
        """
        return copy.copy(self._positions)

    def transaction_iter(self) -> Iterator[Transaction]:
        """Return an iterator to iterate over the transactions of the day.

        Returns:
            Iterator[Transaction]: An iterator over the transactions of the day
        """
        return iter(self._transactions)

    def reconcile(self, positions: Dict[str, float]) -> Dict[str, float]:
        """Return a reconciliation of the Day's positions with the given positions.

        The reconciliation is a mapping between symbol and the difference in
        shares of that symbol between the positions for the day and the given
        positions.

        Args:
            positions (Dict[str, float]): A Dictionary mapping a symbol to a
                quantity of that symbol.

        Returns:
            Dict[str, float]: The reconciliation expressing the difference
                between the day's positions and the specified positions
        """
        keys = set(self._positions.keys()).union(positions.keys())

        result = {}
        for key in keys:
            difference = self._positions.get(key, 0) - positions.get(key, 0)
            if difference == 0:
                continue
            result[key] = difference
        return result
