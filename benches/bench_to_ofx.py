#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Sebastien Rousseau <sebastian.rousseau@gmail.com>
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""What it costs to write an OFX statement, as the statement grows.

A writer runs once per export, on however many transactions the
statement held: a quiet account produces a dozen, a busy one at month
end several thousand. The writer accepts three input shapes, and each
takes a different normalisation path, so all three are measured:

* ``list[Transaction]`` (what the core parsers' ``to_transactions``
  returns);
* ``pandas.DataFrame`` (what the core parsers' ``parse`` returns);
* ``list[dict]`` (records built by hand).

Read ``us/txn``. Flat means linear, and a month-end export is fine.
Climbing means something rescans records it has already written.

Run::

    python benches/bench_to_ofx.py
    python benches/bench_to_ofx.py --json
    python benches/bench_to_ofx.py --quick     # what CI runs

Nothing here asserts a threshold: wall-clock is not comparable between
machines, and a flaky performance gate teaches people to ignore red. CI
runs ``--quick`` so a benchmark that has stopped running against the
current API fails the build instead of rotting into a file that reads as
verified and is not.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections.abc import Callable
from datetime import date
from decimal import Decimal
from pathlib import Path

import pandas as pd
from bankstatementparser.transaction_models import Transaction

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bankstatementparser_writer_ofx import to_ofx  # noqa: E402

SHAPES = ("transactions", "dataframe", "dicts")


def records(count: int) -> list[dict]:
    """``count`` alternating credit and debit records over one month."""
    return [
        {
            "account_id": "FR7630006000011234567890189",
            "currency": "EUR",
            "date": date(2026, 1, (i % 28) + 1),
            "amount": Decimal(f"{(i % 900) + 100}.{i % 100:02d}")
            * (1 if i % 2 else -1),
            "description": f"Payment {i} & co",
            "reference": f"REF-{i:06d}",
        }
        for i in range(count)
    ]


def inputs(count: int) -> dict[str, object]:
    """The same ``count`` records in each of the three input shapes."""
    rows = records(count)
    transactions = [
        Transaction(
            account_id=row["account_id"],
            currency=row["currency"],
            amount=row["amount"],
            booking_date=row["date"],
            description=row["description"],
            reference=row["reference"],
        )
        for row in rows
    ]
    frame = pd.DataFrame(
        [{**row, "amount": float(row["amount"])} for row in rows]
    )
    return {"transactions": transactions, "dataframe": frame, "dicts": rows}


def _best(call: Callable[[], object], repeats: int) -> float:
    """Best-of timing after one untimed warm-up.

    The minimum is the least noisy estimator available; the mean follows
    whatever else the machine happens to be doing.
    """
    call()
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        call()
        samples.append(time.perf_counter() - start)
    return min(samples)


def measure(count: int, repeats: int) -> dict:
    """Time one write per input shape at ``count`` records."""
    row: dict = {"transactions": count}
    for shape, data in inputs(count).items():
        seconds = _best(lambda data=data: to_ofx(data), repeats)
        row[f"{shape}_ms"] = seconds * 1e3
        row[f"{shape}_us_per_txn"] = seconds * 1e6 / count
    row["kib"] = len(to_ofx(records(count)).encode("utf-8")) / 1024
    return row


def run(quick: bool) -> list[dict]:
    """Measure every size; ``quick`` keeps it to what CI can afford."""
    sizes, repeats = ([10, 100], 3) if quick else ([10, 100, 1_000, 10_000], 5)
    return [measure(n, repeats) for n in sizes]


def render(rows: list[dict]) -> None:
    """Print the table and the growth verdict."""
    print(
        f"{'txns':>7}{'KiB':>9}"
        + "".join(f"{shape + ' ms':>17}" for shape in SHAPES)
    )
    for row in rows:
        print(
            f"{row['transactions']:>7}{row['kib']:>9.1f}"
            + "".join(f"{row[shape + '_ms']:>17.2f}" for shape in SHAPES)
        )
    first, last = rows[0], rows[-1]
    for shape in SHAPES:
        drift = last[f"{shape}_us_per_txn"] / first[f"{shape}_us_per_txn"]
        print(
            f"  {shape}: {last[f'{shape}_us_per_txn']:.1f} us/txn at "
            f"{last['transactions']:,}, {drift:.2f}x the cost at "
            f"{first['transactions']:,}"
        )


def main() -> int:
    """Run the benchmark and print a table or JSON."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument(
        "--quick", action="store_true", help="small sizes, as CI runs"
    )
    args = parser.parse_args()
    rows = run(quick=args.quick)
    if args.json:
        json.dump(rows, sys.stdout, indent=1)
        print()
    else:
        render(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
