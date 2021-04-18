from typing import Dict, List

from .transaction import Transaction


class Day:
    _positions: Dict[str, float]
    _transactions: List[Transaction]

    def __init__(self):
        self._positions = {}
        self._transactions = []

    def add_position(self, symbol: str, quantity: float):
        self._positions[symbol] = quantity

    def add_transaction(self, transaction: Transaction):
        self._transactions.append(transaction)
