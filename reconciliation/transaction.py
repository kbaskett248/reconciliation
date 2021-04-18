class Transaction:
    symbol: str
    quantity: float
    value: float

    def __init__(self, symbol: str, quantity: float, value: float):
        self.symbol = symbol
        self.quantity = quantity
        self.value = value

    @classmethod
    def create_transaction(
        cls, operation: str, symbol: str, quantity: float, value: float
    ) -> "Transaction":
        types = {c.__name__.upper(): c for c in cls.__subclasses__()}
        return types[operation](symbol, quantity, value)

    @classmethod
    def from_string(cls, string: str) -> "Transaction":
        symbol, operation, quantity, value = string.split(" ")
        return cls.create_transaction(operation, symbol, float(quantity), float(value))

    def __str__(self):
        return (
            f"{self.__class__.__name__}({self.symbol}, {self.quantity}, {self.value})"
        )


class Sell(Transaction):
    pass


class Buy(Transaction):
    pass


class Deposit(Transaction):
    pass


class Fee(Transaction):
    pass


class Dividend(Transaction):
    pass
