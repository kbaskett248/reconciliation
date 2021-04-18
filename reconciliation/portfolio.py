from typing import Generator, List
import pathlib
import re
from .day import Day
from .transaction import Transaction


class Portfolio:
    heading_matcher = re.compile(r"D(?P<day_num>\d+)-(?P<type>\w+)")
    _days: List[Day]

    def __init__(self):
        self._days = []

    def get_day(self, day_num: int) -> Day:
        while True:
            try:
                return self._days[day_num]
            except IndexError:
                self._days.append(Day())

    @classmethod
    def from_file(cls, path: pathlib.Path) -> "Portfolio":
        with open(path, "r") as file_:
            return cls.from_lines(line.strip() for line in file_.readlines())

    @classmethod
    def from_lines(cls, lines: Generator[str, None, None]) -> "Portfolio":
        portfolio = Portfolio()
        day = None
        type_ = None

        for line in lines:
            match = cls.heading_matcher.fullmatch(line)

            if line == "":
                continue
            elif match is not None:
                day = portfolio.get_day(int(match.group("day_num")))
                type_ = match.group("type")
            elif not day or not type_:
                continue
            elif type_ == "TRN":
                transaction = Transaction.from_string(line)
                day.add_transaction(transaction)
            elif type_ == "POS":
                symbol, quantity = line.split(" ")
                day.add_position(symbol, float(quantity))

        return portfolio
