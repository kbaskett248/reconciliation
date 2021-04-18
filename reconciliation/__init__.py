import pathlib

from reconciliation.portfolio import Portfolio

__version__ = "0.1.0"


def reconcile_file(input_path: pathlib.Path, output_path: pathlib.Path):
    """Compute the reconciliation for the Portfolio from input_path.

    Import the Portfolio from input_path. Then compute the reconciliation over
    the duration of the Portfolio and write it to output_path.

    Args:
        input_path (pathlib.Path): Path to the input file for the Portfolio.
        output_path (pathlib.Path): Output path to write the reconciliation.
    """
    portfolio = Portfolio.from_file(input_path)
    portfolio.reconcile(output_path=output_path)
