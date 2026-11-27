# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Convert a CSV statement to an OFX file and read it back.

Parses ``examples/data/statement.csv`` with the core
``bankstatementparser``, writes it with ``write_ofx`` to a temporary
directory, then parses the OFX file with the core parser again to show
the amounts and IDs survive the round trip.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from bankstatementparser import create_parser

from bankstatementparser_writer_ofx import write_ofx

DATA = Path(__file__).resolve().parent / "data"


def main() -> None:
    """CSV in, OFX out, OFX back in."""
    parser = create_parser(str(DATA / "statement.csv"))
    with tempfile.TemporaryDirectory() as tmp:
        target = write_ofx(
            parser,
            Path(tmp) / "statement.ofx",
            bank_id="30006",
            account_id="FR7630006000011234567890189",
        )
        print(f"Wrote {target.name}: {target.stat().st_size} bytes")
        frame = create_parser(str(target)).parse()
    print(f"Read back {len(frame)} transactions:")
    for row in frame.itertuples():
        print(f"  {row.date}  {row.amount:>9}  {row.transaction_id}")
    print(f"Net movement: {frame['amount'].astype(float).sum():.2f} EUR")


if __name__ == "__main__":
    main()
