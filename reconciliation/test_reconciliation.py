"""This file includes tests for the reconciliation package."""

import pathlib
import unittest

from .account import Account

RECONCILIATION_INPUT = """
D0-POS
AAPL 100
GOOG 200
SP500 175.75
Cash 1000

D1-TRN
AAPL SELL 100 30000
GOOG BUY 10 10000
Cash DEPOSIT 0 1000
Cash FEE 0 50
GOOG DIVIDEND 0 50
TD BUY 100 10000

D1-POS
GOOG 220
SP500 175.75
Cash 20000
MSFT 10
""".lstrip()

RECONCILIATION_OUTPUT = """
Cash 8000
GOOG 10
MSFT 10
TD -100
""".lstrip()

RECONCILIATION_OUTPUT_DICT = {
    key: float(value)
    for key, value in map(lambda l: l.split(), RECONCILIATION_OUTPUT.splitlines())
}


class TestAccount(unittest.TestCase):
    """Test suite for the Account class."""

    def test_reconciliation(self):
        """Verify that reconciliation produces the correct output."""

        account = Account.from_lines(RECONCILIATION_INPUT.splitlines())
        self.assertEqual(account.reconcile(), RECONCILIATION_OUTPUT_DICT)

    def test_reconciliation_file_output(self):
        """Verify that reconciliation produces the correct output file."""
        output_file_path = pathlib.Path("recon.out")
        try:
            account = Account.from_lines(RECONCILIATION_INPUT.splitlines())
            account.reconcile(output_path=output_file_path)

            with open(output_file_path, "r") as file_:
                output = file_.read()

            self.assertEqual(output, RECONCILIATION_OUTPUT)
        finally:
            output_file_path.unlink()

    def test_reconciliation_file_input(self):
        """Verify that reconciliation from an input file produces correct output."""
        input_file_path = pathlib.Path("recon.in")
        try:
            with open(input_file_path, "w") as file_:
                file_.write(RECONCILIATION_INPUT)

            account = Account.from_file(input_file_path)

            self.assertEqual(account.reconcile(), RECONCILIATION_OUTPUT_DICT)
        finally:
            input_file_path.unlink()


if __name__ == "__main__":
    unittest.main()
