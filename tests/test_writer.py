# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Tests for Open Financial Exchange (OFX) Writer."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import pandas as pd
from bankstatementparser.transaction_models import Transaction
from hypothesis import given
from hypothesis import strategies as st

from bankstatementparser_writer_ofx import __version__, to_ofx, write_ofx
from bankstatementparser_writer_ofx.writer import (
    _coerce_amount_decimal,
    _escape_ofx_text,
    _format_ofx_datetime,
    _normalize_records,
)


class DummyParserWithTransactions:
    """Mock parser implementing to_transactions."""

    def to_transactions(self) -> list[Transaction]:
        """Return dummy transactions."""
        return [
            Transaction(
                account_id="ACC01",
                amount=Decimal("120.00"),
                booking_date=date(2026, 1, 1),
                description="Dummy Parser Tx",
            )
        ]


class DummyParserWithDataFrame:
    """Mock parser implementing parse."""

    def parse(self) -> pd.DataFrame:
        """Return dummy DataFrame."""
        return pd.DataFrame(
            [
                {
                    "date": "2026-01-02",
                    "amount": 250.50,
                    "description": "DF Parser Tx",
                }
            ]
        )


def test_version() -> None:
    """Verifies that version is exposed and semantic."""
    assert __version__ == "0.0.19"


def test_to_ofx_with_transactions() -> None:
    """Tests OFX output from Transaction domain models."""
    txs = [
        Transaction(
            account_id="FR76123456789",
            currency="EUR",
            amount=Decimal("2500.00"),
            booking_date=date(2026, 1, 15),
            description="Client Payment & Co",
            reference="REF-001",
        ),
        Transaction(
            account_id="FR76123456789",
            currency="EUR",
            amount=Decimal("-75.30"),
            booking_date=date(2026, 1, 16),
            description="Restaurant <Downtown>",
            reference="REF-002",
        ),
    ]

    out = to_ofx(txs, bank_id="BNPAFR", account_type="CHECKING")

    assert "OFXHEADER:100" in out
    assert "<OFX>" in out
    assert "<CURDEF>EUR" in out
    assert "<BANKID>BNPAFR" in out
    assert "<ACCTID>FR76123456789" in out
    assert "<ACCTTYPE>CHECKING" in out
    assert "<TRNTYPE>CREDIT" in out
    assert "<TRNAMT>2500.00" in out
    assert "<NAME>Client Payment &amp; Co" in out
    assert "<TRNTYPE>DEBIT" in out
    assert "<TRNAMT>-75.30" in out
    assert "<NAME>Restaurant &lt;Downtown&gt;" in out
    assert "<BALAMT>2424.70" in out
    assert "</OFX>" in out


def test_to_ofx_with_dataframe() -> None:
    """Tests OFX output from pandas DataFrame."""
    df = pd.DataFrame(
        [
            {
                "date": "2026-01-20",
                "amount": 500.00,
                "payee": "Direct Deposit",
                "account_id": "ACC-9988",
                "currency": "USD",
            }
        ]
    )

    out = to_ofx(df, currency="USD")
    assert "<CURDEF>USD" in out
    assert "<ACCTID>ACC-9988" in out
    assert "<TRNAMT>500.00" in out


def test_to_ofx_with_dict_records() -> None:
    """Tests OFX output from dictionary rows."""
    records = [
        {
            "booking_date": datetime(2026, 1, 25, 12, 0, 0),
            "amount": "-1,250.75",
            "description": "Monthly Rent",
            "memo": "Apartment 4B",
        }
    ]
    out = to_ofx(records)
    assert "<TRNAMT>-1250.75" in out
    assert "<MEMO>Apartment 4B" in out


def test_write_ofx_file(tmp_path: Path) -> None:
    """Tests writing OFX output to disk."""
    dest = tmp_path / "subdir" / "export.ofx"
    txs = [
        Transaction(
            account_id="ACC99",
            amount=Decimal("50.00"),
            booking_date=date(2026, 2, 1),
            description="Bookstore",
        )
    ]
    path = write_ofx(txs, dest)
    assert path.exists()
    assert "<OFX>" in path.read_text(encoding="utf-8")


def test_dummy_parsers() -> None:
    """Tests parser object duck typing in _normalize_records."""
    p1 = DummyParserWithTransactions()
    r1 = _normalize_records(p1)
    assert len(r1) == 1
    assert r1[0]["payee"] == "Dummy Parser Tx"

    p2 = DummyParserWithDataFrame()
    r2 = _normalize_records(p2)
    assert len(r2) == 1
    assert r2[0]["description"] == "DF Parser Tx"


def test_formatting_edge_cases() -> None:
    """Tests datetime and amount formatting edge cases."""
    assert "[0:UTC]" in _format_ofx_datetime(None)
    assert "[0:UTC]" in _format_ofx_datetime(float("nan"))
    assert "20260228120000[0:UTC]" == _format_ofx_datetime(date(2026, 2, 28))
    assert "20260228103000[0:UTC]" == _format_ofx_datetime(
        datetime(2026, 2, 28, 10, 30, 0)
    )
    assert "20260301120000[0:UTC]" == _format_ofx_datetime("2026-03-01")
    assert "20269999" == _format_ofx_datetime("2026-99-99")
    assert "rawdate" == _format_ofx_datetime("raw-date")
    assert "12345" == _format_ofx_datetime(12345)

    assert _coerce_amount_decimal(None) == Decimal("0.00")
    assert _coerce_amount_decimal(float("nan")) == Decimal("0.00")
    assert _coerce_amount_decimal(100) == Decimal("100.00")
    assert _coerce_amount_decimal(10.5) == Decimal("10.50")
    assert _coerce_amount_decimal("1,500.25") == Decimal("1500.25")
    assert _coerce_amount_decimal("invalid-num") == Decimal("0.00")
    assert _coerce_amount_decimal([123]) == Decimal("0.00")

    assert _escape_ofx_text(None) == ""
    assert _escape_ofx_text("A & B < C > D") == "A &amp; B &lt; C &gt; D"


def test_empty_records_ofx() -> None:
    """Tests empty transactions list in to_ofx."""
    out = to_ofx([])
    assert "<OFX>" in out
    assert "<BALAMT>0.00" in out


@given(
    amount=st.decimals(
        min_value=Decimal("-999999.99"),
        max_value=Decimal("999999.99"),
        places=2,
    ),
    payee=st.text(min_size=1, max_size=30).filter(lambda s: "\x00" not in s),
)
def test_fuzz_to_ofx(amount: Decimal, payee: str) -> None:
    """Property-based fuzzing of to_ofx generation."""
    txs = [
        Transaction(
            account_id="FUZZ_ACC",
            amount=amount,
            booking_date=date(2026, 1, 1),
            description=payee,
        )
    ]
    out = to_ofx(txs)
    assert "<OFX>" in out
    assert "</OFX>" in out
