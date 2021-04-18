import copy
from typing import Dict, Iterator, List, Tuple

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
