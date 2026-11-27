# Usage

## Inputs

`to_ofx(data, ...)` and `write_ofx(data, destination, ...)` accept:

- a list of `bankstatementparser` `Transaction` objects;
- a pandas DataFrame, each row a record;
- a list of mappings (dicts);
- any object with a `to_transactions()` method, or a `parse()` method
  returning a DataFrame (the core parsers), which is called first.

Items in a list that are neither a `Transaction` nor a mapping are
skipped.

## Field mapping

| OFX element | Taken from |
| :--- | :--- |
| `<TRNAMT>` | `amount`, to two decimals; unparseable, NaN, infinite or out-of-range (beyond 28 significant digits at cent precision) amounts become `0.00` |
| `<TRNTYPE>` | `CREDIT` when the amount is above zero, otherwise `DEBIT` |
| `<DTPOSTED>` | `date`, else `booking_date`, else `value_date` (a `Transaction` gives its booking date, else its value date), as `YYYYMMDD120000[0:UTC]`; a `datetime` keeps its time, another string is written with `-`, `:` and spaces removed, and no date gives the current time |
| `<FITID>` | `transaction_id`, else `reference`, else `TX-000001` by position (a `Transaction` without an ID gives its `transaction_hash`) |
| `<NAME>` | `payee`, else `description`, else `Transaction` |
| `<MEMO>` | `memo`, else `reference`; omitted when both are empty |
| `<DTSTART>`, `<DTEND>` | the earliest and latest record dates (the current time when none) |
| `<BALAMT>` | the sum of the written amounts |

## Options

| Argument | Default | Meaning |
| :--- | :--- | :--- |
| `bank_id` | `"123456789"` | `<BANKID>` |
| `account_id` | `None` | `<ACCTID>`; when `None`, the first record's `account_id`, else `0000000000` |
| `account_type` | `"CHECKING"` | `<ACCTTYPE>`, e.g. `SAVINGS`, `CREDITLINE` |
| `currency` | `"EUR"` | `<CURDEF>`; while it is `EUR` (the default, or passed explicitly), the last record's `currency` wins |

`write_ofx` writes UTF-8 text to `destination`, creating missing parent
directories, and returns the `Path`.

## Limits

- Only OFX 1.02 SGML is written; there is no OFX 2.x XML output.
- The header declares `ENCODING:USASCII` and `CHARSET:1252`, but the
  text is written as UTF-8, so non-ASCII names may be misread by a strict
  importer.
- `<LEDGERBAL>` is the sum of the transactions, not a balance from your
  bank.
- `<TRNTYPE>` is `CREDIT` or `DEBIT` only.
