"""This module provides a Transaction class and subclasses."""

from abc import abstractmethod
from typing import Dict


class Transaction:
    """Class representing a transaction that can be applied to your positions.

    This is a parent class which is subclassed by the concrete transaction
    types below. Each subclass implements the apply method, which mutates a
    dictionary of positions according to the transaction.

    Instead of creating a Transaction directly, use the create_transaction
    class method. This factory function will select the appropriate subclass
    and return an instance of that subclass.

    Attributes:
        quantity [float]: The number of shares transacted
        symbol [str]: The unique identifier symbol that this Transaction
            modifies
        value [float]: The value of the transaction
    """

    symbol: str
    quantity: float
    value: float

    def __init__(self, symbol: str, quantity: float, value: float):
        self.symbol = symbol
        self.quantity = quantity
        self.value = value

    @abstractmethod
    def apply(self, positions: Dict[str, float]):
        """Apply the transaction by mutating the given dictionary of positions.

        This method should be implemented in any subclass.

        Args:
            positions (Dict[str, float]): A dictionary mapping a symbol to
                the number of shares, or, in the case of Cash, the amount of
                cash in the account.
        """
        pass

    @classmethod
    def create_transaction(
        cls, operation: str, symbol: str, quantity: float, value: float
    ) -> "Transaction":
        """Creates a transaction for the given operation.

        This method selects the appropriate subclass of Transaction by matching
        the name of the class with the string representation.

        Returns:
            Transaction: A Transaction instance with the given data
        """
        types = {c.__name__.upper(): c for c in cls.__subclasses__()}
        return types[operation.upper()](symbol, quantity, value)

    @classmethod
    def from_string(cls, string: str) -> "Transaction":
        """Create a transaction for the given text line.

        The input is expected to be in the form:
        <Symbol> <Operation> <Quantity> <Value>

        Returns:
            Transaction: A Transaction instance with the given data
        """
        symbol, operation, quantity, value = string.split(" ")
        return cls.create_transaction(operation, symbol, float(quantity), float(value))

    def __str__(self) -> str:
        """Format a string representation of the Transaction.

        Returns:
            str: A string describing the Transaction
        """
        return (
            f"{self.__class__.__name__}({self.symbol}, {self.quantity}, {self.value})"
        )


class Sell(Transaction):
    """Class representing a Sell transaction.

    Sell decreases shares of symbol by quantity and increases Cash by value.

    Attributes:
        quantity [float]: The number of shares sold
        symbol [str]: The symbol of the shares sold
        value [float]: The value of the sell
    """

    def apply(self, positions: Dict[str, float]):
        """Apply the Sell transaction by mutating positions.

        Decrease shares of symbol by quantity and increase Cash by value.

        Args:
            positions (Dict[str, float]): A dictionary mapping a symbol to
                the number of shares, or, in the case of Cash, the amount of
                cash in the account.
        """
        positions[self.symbol] = positions.get(self.symbol, 0) - self.quantity
        positions["Cash"] = positions.get("Cash", 0) + self.value


class Buy(Transaction):
    """Class representing a Buy transaction.

    Buy increases shares of symbol by quantity and decreases Cash by value.

    Attributes:
        quantity [float]: The number of shares bought
        symbol [str]: The symbol of the shares bought
        value [float]: The value of the buy
    """

    def apply(self, positions: Dict[str, float]):
        """Apply the Buy transaction by mutating positions.

        Increase shares of symbol by quantity and decrease Cash by value.

        Args:
            positions (Dict[str, float]): A dictionary mapping a symbol to
                the number of shares, or, in the case of Cash, the amount of
                cash in the account.
        """
        positions[self.symbol] = positions.get(self.symbol, 0) + self.quantity
        positions["Cash"] = positions.get("Cash", 0) - self.value


class Deposit(Transaction):
    """Class representing a Deposit transaction.

    Deposit increases Cash by value.

    Attributes:
        quantity [float]: Will be 0
        symbol [str]: Will be Cash
        value [float]: The amount deposited
    """

    def apply(self, positions: Dict[str, float]):
        """Apply the Deposit transaction by mutating positions.

        Increase Cash by value.

        Args:
            positions (Dict[str, float]): A dictionary mapping a symbol to
                the number of shares, or, in the case of Cash, the amount of
                cash in the account.
        """
        positions[self.symbol] = positions.get(self.symbol, 0) + self.value


class Fee(Transaction):
    """Class representing a Fee transaction.

    Fee decreases Cash by value.

    Attributes:
        quantity [float]: Will be 0
        symbol [str]: Will be Cash
        value [float]: The price of the fee
    """

    def apply(self, positions: Dict[str, float]):
        """Apply the Fee transaction by mutating positions.

        Decrease Cash by value.

        Args:
            positions (Dict[str, float]): A dictionary mapping a symbol to
                the number of shares, or, in the case of Cash, the amount of
                cash in the account.
        """
        positions[self.symbol] = positions.get(self.symbol, 0) - self.value


class Dividend(Transaction):
    """Class representing a Dividend transaction.

    Dividend is associated with a symbol and increases Cash by value.

    Attributes:
        quantity [float]: Will be 0
        symbol [str]: The symbol of the shares that produced the dividend
        value [float]: The value of the dividend
    """

    def apply(self, positions: Dict[str, float]):
        """Apply the Dividend transaction by mutating positions.

        Increase Cash by value.

        Args:
            positions (Dict[str, float]): A dictionary mapping a symbol to
                the number of shares, or, in the case of Cash, the amount of
                cash in the account.
        """
        positions["Cash"] = positions.get("Cash", 0) + self.value
