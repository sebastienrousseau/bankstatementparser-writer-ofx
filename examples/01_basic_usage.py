# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Serialise Transaction objects to an OFX 1.02 document.

Builds two ``bankstatementparser`` transactions and prints the
``<STMTTRN>`` blocks and the ledger balance ``to_ofx`` writes for them.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from bankstatementparser.transaction_models import Transaction

from bankstatementparser_writer_ofx import to_ofx


def main() -> None:
    """Write two transactions and show the statement part of the OFX."""
    transactions = [
        Transaction(
            account_id="FR7630006000011234567890189",
            amount=Decimal("150.00"),
            currency="EUR",
            booking_date=date(2026, 1, 15),
            description="Invoice 1024 & 1025",
            transaction_id="E2E-001",
        ),
        Transaction(
            account_id="FR7630006000011234567890189",
            amount=Decimal("-42.50"),
            currency="EUR",
            booking_date=date(2026, 1, 16),
            description="Card payment",
            reference="CARD-0116",
        ),
    ]
    ofx = to_ofx(transactions, bank_id="30006")
    lines = ofx.splitlines()
    start = lines.index("<BANKACCTFROM>")
    end = lines.index("</LEDGERBAL>")
    print(f"to_ofx wrote {len(lines)} lines; the statement part:")
    for line in lines[start : end + 1]:
        if not line.startswith("<DTASOF>"):
            print(f"  {line}")


if __name__ == "__main__":
    main()
