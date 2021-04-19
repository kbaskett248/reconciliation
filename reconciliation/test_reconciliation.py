"""This file includes tests for the reconciliation package."""

import pathlib
import unittest

from . import reconcile_file

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


class TestAccount(unittest.TestCase):
    """Test suite for the Account class."""

    def test_reconciliation(self):
        """Verify that reconciliation produces the correct output file."""

        input_file_path = pathlib.Path("recon.in")
        output_file_path = pathlib.Path("recon.out")
        try:
            with open(input_file_path, "w") as file_:
                file_.write(RECONCILIATION_INPUT)

            reconcile_file(input_file_path, output_file_path)

            with open(output_file_path, "r") as file_:
                output = file_.read()

            self.assertEqual(output, RECONCILIATION_OUTPUT)
        finally:
            input_file_path.unlink()
            output_file_path.unlink()


if __name__ == "__main__":
    unittest.main()
