# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Basic usage example for bankstatementparser-writer-ofx."""

from decimal import Decimal

from bankstatementparser.transaction_models import Transaction


def main() -> None:
    print("Running basic bankstatementparser-writer-ofx demonstration...")
    txns = [
        Transaction(
            account_id="ACC-001",
            amount=Decimal("150.00"),
            currency="EUR",
            description="Payment sample",
            reference="REF-001",
        )
    ]
    print(f"Input: {len(txns)} transactions")


if __name__ == "__main__":
    main()
