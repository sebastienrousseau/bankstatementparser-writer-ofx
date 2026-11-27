# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Structured Open Financial Exchange (OFX) Writer."""

from __future__ import annotations

import os
from collections.abc import Mapping, Sequence
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

import pandas as pd
from bankstatementparser.transaction_models import Transaction

__all__ = ["to_ofx", "write_ofx"]


def _format_ofx_datetime(val: Any) -> str:
    """Format dates to OFX standard timestamp YYYYMMDDHHMMSS[0:UTC] or YYYYMMDD."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        now = datetime.now(timezone.utc)
        return now.strftime("%Y%m%d120000[0:UTC]")
    if isinstance(val, datetime):
        return val.strftime("%Y%m%d%H%M%S[0:UTC]")
    if isinstance(val, date):
        return val.strftime("%Y%m%d120000[0:UTC]")
    if isinstance(val, str):
        clean = val.strip()
        if len(clean) >= 10 and clean[4] == "-" and clean[7] == "-":
            try:
                d = date.fromisoformat(clean[:10])
                return d.strftime("%Y%m%d120000[0:UTC]")
            except ValueError:
                return clean.replace("-", "").replace(":", "").replace(" ", "")
        return clean.replace("-", "").replace(":", "").replace(" ", "")
    return str(val)


def _coerce_amount_decimal(val: Any) -> Decimal:
    """Coerce various amount types to a finite Decimal.

    A NaN or infinite amount becomes 0.00, as an unparseable one does:
    OFX has no way to write either, and a NaN Decimal raises on the
    credit/debit comparison.
    """
    amount = _parse_amount(val)
    return amount if amount.is_finite() else Decimal("0.00")


def _parse_amount(val: Any) -> Decimal:
    """Parse the supported amount types to Decimal (possibly non-finite)."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return Decimal("0.00")
    if isinstance(val, Decimal):
        return val
    if isinstance(val, (int, float)):
        return Decimal(f"{val:.2f}")
    if isinstance(val, str):
        clean = val.strip().replace(",", "")
        try:
            return Decimal(clean)
        except Exception:
            return Decimal("0.00")
    return Decimal("0.00")


def _escape_ofx_text(val: Any) -> str:
    """Escape XML special characters for OFX."""
    if val is None:
        return ""
    text = str(val).strip().replace("\n", " ")
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _normalize_records(
    data: (
        Sequence[Transaction]
        | pd.DataFrame
        | Sequence[Mapping[str, Any]]
        | Any
    ),
) -> list[dict[str, Any]]:
    """Normalize supported data inputs into standard dictionary rows."""
    data_any: Any = data
    if hasattr(data_any, "to_transactions") and callable(
        data_any.to_transactions
    ):
        txs = data_any.to_transactions()
        return _normalize_records(txs)

    if hasattr(data_any, "parse") and callable(data_any.parse):
        df = data_any.parse()
        return _normalize_records(df)

    if isinstance(data, pd.DataFrame):
        records = []
        for _, row in data.iterrows():
            rec = row.to_dict()
            records.append(rec)
        return records

    records = []
    for item in data:
        if isinstance(item, Transaction):
            records.append(
                {
                    "account_id": item.account_id,
                    "currency": item.currency,
                    "date": item.booking_date or item.value_date,
                    "amount": item.amount,
                    "payee": item.description,
                    "reference": item.reference,
                    "transaction_id": item.transaction_id
                    or item.transaction_hash,
                }
            )
        elif isinstance(item, Mapping):
            records.append(dict(item))
    return records


_HEADER = """OFXHEADER:100
DATA:OFXSGML
VERSION:102
SECURITY:NONE
ENCODING:USASCII
CHARSET:1252
COMPRESSION:NONE
OLDFILEUID:NONE
NEWFILEUID:NONE

<OFX>
<SIGNONMSGSRSV1>
<SONRS>
<STATUS>
<CODE>0
<SEVERITY>INFO
</STATUS>
<DTSERVER>{now}
<LANGUAGE>ENG
</SONRS>
</SIGNONMSGSRSV1>
<BANKMSGSRSV1>
<STMTTRNRS>
<TRNUID>1
<STATUS>
<CODE>0
<SEVERITY>INFO
</STATUS>
<STMTRS>
<CURDEF>{currency}
<BANKACCTFROM>
<BANKID>{bank_id}
<ACCTID>{account_id}
<ACCTTYPE>{account_type}
</BANKACCTFROM>
<BANKTRANLIST>
<DTSTART>{start}
<DTEND>{end}
"""

_FOOTER = """</BANKTRANLIST>
<LEDGERBAL>
<BALAMT>{total:.2f}
<DTASOF>{now}
</LEDGERBAL>
</STMTRS>
</STMTTRNRS>
</BANKMSGSRSV1>
</OFX>
"""


def _record_date(rec: Mapping[str, Any]) -> Any:
    """The record's date: ``date``, else ``booking_date``, else ``value_date``."""
    return rec.get("date") or rec.get("booking_date") or rec.get("value_date")


def _infer_account_and_currency(
    records: list[dict[str, Any]], account_id: str | None, currency: str
) -> tuple[str, str]:
    """Fill the account from the first record that has one, and the
    currency from the last, when the caller left the default ``EUR``."""
    inferred_acct = account_id
    inferred_curr = currency
    for rec in records:
        if not inferred_acct and rec.get("account_id"):
            inferred_acct = str(rec["account_id"])
        if currency == "EUR" and rec.get("currency"):
            inferred_curr = str(rec["currency"])
    return inferred_acct or "0000000000", inferred_curr


def _date_range(records: list[dict[str, Any]], now: str) -> tuple[str, str]:
    """Earliest and latest formatted record date, or ``now`` for both."""
    dates = [
        _format_ofx_datetime(_record_date(rec))
        for rec in records
        if _record_date(rec) is not None
    ]
    if not dates:
        return now, now
    return min(dates), max(dates)


def _transaction_lines(idx: int, rec: Mapping[str, Any]) -> list[str]:
    """The ``<STMTTRN>`` block for one record, every value escaped."""
    amt = _coerce_amount_decimal(rec.get("amount"))
    fitid = (
        rec.get("transaction_id")
        or rec.get("reference")
        or f"TX-{idx + 1:06d}"
    )
    name = rec.get("payee") or rec.get("description") or "Transaction"
    memo = rec.get("memo") or rec.get("reference") or ""
    lines = [
        "<STMTTRN>",
        f"<TRNTYPE>{'CREDIT' if amt > 0 else 'DEBIT'}",
        f"<DTPOSTED>{_escape_ofx_text(_format_ofx_datetime(_record_date(rec)))}",
        f"<TRNAMT>{amt:.2f}",
        f"<FITID>{_escape_ofx_text(fitid)}",
        f"<NAME>{_escape_ofx_text(name)}",
    ]
    if memo:
        lines.append(f"<MEMO>{_escape_ofx_text(memo)}")
    lines.append("</STMTTRN>")
    return lines


def to_ofx(
    data: (
        Sequence[Transaction]
        | pd.DataFrame
        | Sequence[Mapping[str, Any]]
        | Any
    ),
    bank_id: str = "123456789",
    account_id: str | None = None,
    account_type: str = "CHECKING",
    currency: str = "EUR",
) -> str:
    """Serialise bank transactions into standard OFX 1.02 format.

    Every value taken from the records or the arguments is escaped, so
    record text can never open or close an OFX element.

    Args:
        data: Transactions as DataFrame, Transaction list, or dict records.
        bank_id: Routing / Bank identifier.
        account_id: Account identifier (inferred from first transaction if None).
        account_type: Account type (default 'CHECKING', e.g. 'SAVINGS', 'CREDITLINE').
        currency: ISO 4217 Currency code (default 'EUR').

    Returns:
        Formatted OFX document string.
    """
    records = _normalize_records(data)
    now = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S[0:UTC]")
    acct, curr = _infer_account_and_currency(records, account_id, currency)
    start, end = _date_range(records, now)
    header = _HEADER.format(
        now=now,
        currency=_escape_ofx_text(curr),
        bank_id=_escape_ofx_text(bank_id),
        account_id=_escape_ofx_text(acct),
        account_type=_escape_ofx_text(account_type),
        start=_escape_ofx_text(start),
        end=_escape_ofx_text(end),
    )
    body: list[str] = []
    for idx, rec in enumerate(records):
        body.extend(_transaction_lines(idx, rec))
    total = sum(
        (_coerce_amount_decimal(rec.get("amount")) for rec in records),
        Decimal("0.00"),
    )
    return (
        header + "\n".join(body) + "\n" + _FOOTER.format(total=total, now=now)
    )


def write_ofx(
    data: (
        Sequence[Transaction]
        | pd.DataFrame
        | Sequence[Mapping[str, Any]]
        | Any
    ),
    destination: str | os.PathLike[str],
    bank_id: str = "123456789",
    account_id: str | None = None,
    account_type: str = "CHECKING",
    currency: str = "EUR",
) -> Path:
    """Write transactions to an OFX file on disk.

    Args:
        data: Transactions as DataFrame, Transaction list, or dict records.
        destination: Filesystem destination path.
        bank_id: Routing / Bank identifier.
        account_id: Account identifier.
        account_type: Account type.
        currency: ISO Currency code.

    Returns:
        Path object pointing to the written file.
    """
    content = to_ofx(
        data,
        bank_id=bank_id,
        account_id=account_id,
        account_type=account_type,
        currency=currency,
    )
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target
