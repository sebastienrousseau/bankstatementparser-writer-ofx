# Open Financial Exchange (OFX) Writer for Bank Statement Parser

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0_OR_MIT-blue.svg)](LICENSE)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/sebastienrousseau/bankstatementparser-writer-ofx)

Open Financial Exchange (OFX) export writer plugin for [`bankstatementparser`](https://github.com/sebastienrousseau/bankstatementparser).

---

## Features

- **Standard OFX 1.02 Serialization**: Generates clean, compliant OFX files compatible with Quicken, QuickBooks, Xero, Sage, Money, and standard accounting software.
- **Multiple Input Shapes**: Seamlessly accepts `list[Transaction]`, `pandas.DataFrame`, `list[dict]`, or any `bankstatementparser` statement parser object.
- **Configurable Headers**: Customize bank routing ID, account ID, account type (`CHECKING`, `SAVINGS`, `CREDITLINE`), and currency.
- **100% Type Safe & Tested**: Full static typing and 100% test coverage.

---

## Installation

```bash
pip install bankstatementparser-writer-ofx
```

---

## Quickstart

```python
from bankstatementparser.transaction_models import Transaction
from bankstatementparser_writer_ofx import write_ofx
from decimal import Decimal
from datetime import date

transactions = [
    Transaction(
        account_id="FR76123456789",
        amount=Decimal("2500.00"),
        currency="EUR",
        booking_date=date(2026, 1, 15),
        description="Client Payment & Co",
        reference="REF-001",
    ),
    Transaction(
        account_id="FR76123456789",
        amount=Decimal("-75.30"),
        currency="EUR",
        booking_date=date(2026, 1, 16),
        description="Restaurant Downtown",
        reference="REF-002",
    ),
]

# Write to OFX file
write_ofx(transactions, "statement.ofx", bank_id="123456789")
```

---

## License

Dual-licensed under Apache 2.0 and MIT.
