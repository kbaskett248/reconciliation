import pathlib
import unittest

from .portfolio import Portfolio

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
"""

RECONCILIATION_OUTPUT = """
Cash 8000
GOOG 10
TD -100
MSFT 10
"""


class TestPortfolio(unittest.TestCase):
    """Test suite for the Portfolio class."""

    def test_reconciliation(self):
        """Verify that reconciliation produces the correct output file."""

        input_file_path = pathlib.Path("recon.in")
        try:
            with open(input_file_path, "w") as file_:
                file_.write(RECONCILIATION_INPUT)

            portfolio = Portfolio.from_file(input_file_path)
        finally:
            input_file_path.unlink()

        output_file_path = pathlib.Path("recon.out")
        try:
            portfolio.reconcile(1, output_file_path)

            with open(output_file_path, "r") as file_:
                output = file_.read()

            self.assertEqual(output, RECONCILIATION_OUTPUT)
        finally:
            output_file_path.unlink()


if __name__ == "__main__":
    unittest.main()
