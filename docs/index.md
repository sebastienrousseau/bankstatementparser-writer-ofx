# bankstatementparser-writer-ofx

**OFX** (Open Financial Exchange) is the statement format that
accounting and personal-finance software imports.
**bankstatementparser-writer-ofx** writes transactions parsed by
[`bankstatementparser`](https://github.com/sebastienrousseau/bankstatementparser)
as an OFX 1.02 (SGML) bank statement: one `<STMTTRN>` per transaction
inside `<BANKMSGSRSV1><STMTTRNRS><STMTRS>`, with a ledger balance.

| Concern | How this writer handles it |
| :--- | :--- |
| Input | `list[Transaction]`, a `pandas.DataFrame`, `list[dict]`, or a core parser object |
| Structure | `<SIGNONMSGSRSV1>`, `<BANKMSGSRSV1>`, `<STMTRS>`, `<BANKTRANLIST>` and `<LEDGERBAL>` |
| Transactions | `<TRNTYPE>` (`CREDIT` or `DEBIT`), `<DTPOSTED>`, `<TRNAMT>`, `<FITID>`, `<NAME>` and an optional `<MEMO>` |
| Safety | `&`, `<` and `>` escaped in every value; NaN, infinite and out-of-range amounts written as `0.00` |

```python
from bankstatementparser import create_parser

from bankstatementparser_writer_ofx import write_ofx

parser = create_parser("statement.csv")
write_ofx(parser, "statement.ofx", bank_id="30006", account_id="12345678")
```

## In this manual

- [Usage](usage.md): inputs, field mapping, options and limits.
- [Architecture](architecture.md): how the module is laid out.
- [The suite](suite.md): the `bankstatementparser` packages.
- [Comparison](COMPARISON.md) and [Benchmarks](BENCHMARKS.md).
- [Supported Python policy](POLICIES.md).
- [API reference](api.md), generated from the docstrings.
- [Changelog](changelog.md) and [Security policy](security.md).

The source, issues and releases live on
[GitHub](https://github.com/sebastienrousseau/bankstatementparser-writer-ofx);
the package is on
[PyPI](https://pypi.org/project/bankstatementparser-writer-ofx/).
