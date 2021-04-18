import pathlib

from reconciliation.account import Account

__version__ = "0.1.0"


def reconcile_file(input_path: pathlib.Path, output_path: pathlib.Path):
    """Compute the reconciliation for the Account from input_path.

    Import the Account from input_path. Then compute the reconciliation over
    the duration of the Account and write it to output_path.

    Args:
        input_path (pathlib.Path): Path to the input file for the Account.
        output_path (pathlib.Path): Output path to write the reconciliation.
    """
    account = Account.from_file(input_path)
    account.reconcile(output_path=output_path)
