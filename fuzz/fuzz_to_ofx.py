# SPDX-FileCopyrightText: 2026 Sebastien Rousseau <sebastian.rousseau@gmail.com>
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Coverage-guided Atheris fuzz target for the OFX writer.

``to_ofx`` takes records from a parsed statement (dicts here, the most
permissive input it accepts) whose amounts, dates and text come from
whatever bank produced the file. Whatever the record holds, it must
return an OFX document the reader at the other end can parse:

* it never raises;
* it writes one ``<STMTTRN>`` block per record;
* every ``<TRNAMT>`` and ``<BALAMT>`` is a plain two-decimal number;
* every element line is one tag and a value with no markup characters,
  so record text can never open or close an element.

Any exception, or a broken invariant, escapes the target and libFuzzer
records it as a crash.

Run (Linux x86_64, Python 3.12+, ``poetry install --with fuzz``)::

    python fuzz/fuzz_to_ofx.py fuzz/corpus -max_total_time=60
"""

from __future__ import annotations

import re
import sys

import atheris

with atheris.instrument_imports():
    from bankstatementparser_writer_ofx import to_ofx

_FIELDS = (
    "amount",
    "date",
    "payee",
    "memo",
    "reference",
    "transaction_id",
    "account_id",
    "currency",
)
_AMOUNT = re.compile(r"-?\d+\.\d\d")
_ELEMENT = re.compile(r"<([A-Z0-9.]+)>([^<>]*)")


def _records(fdp: atheris.FuzzedDataProvider) -> list[dict[str, str]]:
    """Build up to four records whose fields are fuzzed strings."""
    records = []
    for _ in range(fdp.ConsumeIntInRange(0, 4)):
        records.append(
            {
                name: fdp.ConsumeUnicodeNoSurrogates(24)
                for name in _FIELDS
                if fdp.ConsumeBool()
            }
        )
    return records


def _check(ofx: str, count: int) -> None:
    """Fail unless ``ofx`` is well-formed for ``count`` records."""
    if ofx.count("<STMTTRN>") != count:
        raise AssertionError(
            f"{ofx.count('<STMTTRN>')} blocks, {count} records"
        )
    for line in ofx.split("\n"):
        if not line.startswith("<") or line.startswith("</"):
            continue
        match = _ELEMENT.fullmatch(line)
        if match is None:
            raise AssertionError(f"markup in element line {line!r}")
        tag, value = match.groups()
        if tag in ("TRNAMT", "BALAMT") and not _AMOUNT.fullmatch(value):
            raise AssertionError(f"{tag} is {value!r}")


def test_one_input(data: bytes) -> None:
    """Write one fuzzed batch of records and check the document."""
    fdp = atheris.FuzzedDataProvider(data)
    records = _records(fdp)
    _check(to_ofx(records), len(records))


def main() -> None:
    """Hand the target to libFuzzer with the command-line options."""
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
