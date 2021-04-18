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
    def test_reconciliation(self):
        try:
            with open("recon.in", "w") as file_:
                file_.write(RECONCILIATION_INPUT)

            portfolio = Portfolio.from_file("recon.in")
        finally:
            pathlib.Path("recon.in").unlink()
        
        try:
            portfolio.reconcile(1).to_file("recon.out")

            with open("recon.out", "r") as file_:
                output = file_.read()

            self.assertEqual(output, RECONCILIATION_OUTPUT)
        finally:
            pathlib.Path("recon.out").unlink()


if __name__ == "__main__":
    unittest.main()
