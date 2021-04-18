import pathlib
import re
from typing import Dict, Iterable, List, Optional

from .day import Day
from .transaction import Transaction


class Portfolio:
    """Class representing a portfolio over one or more days.

    The portfolio stores a number of days, accessible via the offset since the
    Portfolio was started. Each Day stores the transactions that occurred that
    day and the positions at the end of the day.

    """

    heading_matcher = re.compile(r"D(?P<day_num>\d+)-(?P<type>\w+)")
    _days: List[Day]

    def __init__(self):
        self._days = []

    def get_day(self, day_num: int) -> Day:
        """Return the nth day since the Portfolio was opened.

        Args:
            day_num (int): The day offset to return

        Returns:
            Day: The nth Day in the Portfolio
        """
        while True:
            try:
                return self._days[day_num]
            except IndexError:
                self._days.append(Day())

    def reconcile(
        self, start_day: int = 0, end_day: int = -1, output_path: pathlib.Path = None
    ) -> Optional[Dict[str, float]]:
        """Reconcile the positions and transactions in the Portfolio.

        Apply the transactions from start_day to end_day to the positions on
        start_day. Then return the difference between the positions on end_day
        with the computed positions.

        Args:
            start_day (int, optional): Start with this day's positions when
                computing positions. The transactions from each successive day
                will be applied to these positions. Defaults to 0.
            end_day (int): End with this day when computing reconciliation. The
                positions on this day will be compared to the computed positions.
                Slicing is used, so negative offsets can be used. Defaults to
                -1.
            output_path (pathlib.Path, optional): If specified, write the
                output to the specified path. Defaults to None. Output is
                written as follows:

                <Symbol> <Difference>
                <Symbol> <Difference>
                ...

        Returns:
            Dict[str, float]: A dictionary mapping a symbol to the difference
                between the day's position and the computed position for that
                symbol
        """
        if end_day < 0:
            end_day = len(self._days) + end_day

        # Starting positions
        positions = self.get_day(start_day).get_positions()

        # Apply transactions successively to starting positions
        for day in (self.get_day(i) for i in range(start_day + 1, end_day + 1)):
            for transaction in day.transaction_iter():
                transaction.apply(positions)

        # Reconcile the computed positions with the positions on end_day
        recon = self.get_day(end_day).reconcile(positions)

        if output_path:
            with open(output_path, "w") as file_:
                for key, value in sorted(recon.items()):
                    file_.write(f"{key} {value:g}\n")

        return recon

    @classmethod
    def from_file(cls, path: pathlib.Path) -> "Portfolio":
        """Initialize a new Portfolio by reading an input file.

        The file format is as follows. D0-POS means the positions on Day 0.
        D1-TRN means the transactions on Day 1.

        ```
        D0-POS
        <Symbol> <Quantity>
        <Symbol> <Quantity>
        ...

        D1-TRN
        <Symbol> <Operation> <Quantity> <Value>
        <Symbol> <Operation> <Quantity> <Value>
        ...

        D1-POS
        <Symbol> <Quantity>
        <Symbol> <Quantity>
        ...

        ...
        ```

        Returns:
            Portfolio: A Portfolio object containing the Days defined by the
                input file
        """
        with open(path, "r") as file_:
            return cls.from_lines(line.strip() for line in file_.readlines())

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Portfolio":
        """Initialize a new Portfolio by parsing the given lines.

        The lines should match the following format. D0-POS means the positions
        on Day 0. D1-TRN means the transactions on Day 1.

        ```
        D0-POS
        <Symbol> <Quantity>
        <Symbol> <Quantity>
        ...

        D1-TRN
        <Symbol> <Operation> <Quantity> <Value>
        <Symbol> <Operation> <Quantity> <Value>
        ...

        D1-POS
        <Symbol> <Quantity>
        <Symbol> <Quantity>
        ...

        ...
        ```

        Returns:
            Portfolio: A Portfolio object containing the Days defined by the
                input file
        """
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
