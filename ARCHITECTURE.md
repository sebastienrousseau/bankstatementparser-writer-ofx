<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# bankstatementparser-writer-ofx Architecture

A map of the codebase for contributors. The package is one module of
pure functions; the only I/O is `write_ofx` writing the finished text.

## The flow

```text
list[Transaction] | DataFrame | list[dict] | core parser
        |
        v
_normalize_records()            -> list[dict]
        |
        +-> _infer_account_and_currency()   <ACCTID>, <CURDEF>
        +-> _date_range()                   <DTSTART>, <DTEND>
        +-> _transaction_lines() per record <STMTTRN> ... </STMTTRN>
        |       _coerce_amount_decimal()    finite Decimal or 0.00
        |       _format_ofx_datetime()      YYYYMMDDHHMMSS[0:UTC]
        |       _escape_ofx_text()          & < > escaped, newlines removed
        v
to_ofx(): _HEADER + blocks + _FOOTER (<LEDGERBAL> = sum of amounts)  -> str
write_ofx(): to_ofx() -> UTF-8 file                                  -> Path
```

## Module map

| Area | Path | Responsibility |
| :--- | :--- | :--- |
| **Writer** | `bankstatementparser_writer_ofx/writer.py` | Input normalisation, field formatting and escaping, `to_ofx`, `write_ofx` |
| **Version** | `bankstatementparser_writer_ofx/__init__.py` | `__version__` and the public re-exports |
| **Tests** | `tests/` | Writer behaviour (including Hypothesis properties), concurrency and stress, examples, release notes and the suite's vendored conformance checks; 100% line and branch coverage |
| **Fuzzing** | `fuzz/fuzz_to_ofx.py`, `fuzz/corpus/` | Atheris target for `to_ofx`, run by the CI `Fuzz (Atheris)` job |
| **Benchmarks** | `benches/bench_to_ofx.py` | `to_ofx` cost by input shape and size |
| **Examples** | `examples/`, `examples/data/` | Transactions to OFX, and a CSV-to-OFX round trip |
| **Manual** | `mkdocs.yml`, `docs/` | MkDocs Material user manual and API reference, deployed to GitHub Pages |
| **Release helpers** | `scripts/` | `verify_versions.py`, `release_notes.py`, `export_locked_requirements.py` (hashed exports of `poetry.lock` into `requirements/`), `check_complexity.py`, `check_suite_consistency.py`, `readme-check.sh` |

## Design decisions

- **One normalised shape.** Every input becomes a list of dicts first,
  so the formatting code has one path whatever the caller passed.
- **Escape at the edge.** Every value from the records or the arguments
  goes through `_escape_ofx_text` as it is placed in the document; the
  fuzz target checks no element value carries markup.
- **Never raise on a bad value.** An unparseable, NaN, infinite or
  out-of-range amount
  becomes `0.00` and a missing date becomes the current time, so one
  odd row cannot abort an export; the cost is that bad input is not
  reported.

## CI

`ci.yml` runs the tests on ubuntu, macOS and Windows with CPython 3.10
to 3.14, plus lint, types, Bandit, the complexity baseline, the
examples, the fuzz target and a wheel smoke test. `docs.yml` builds the
manual with `--strict`; `docs-lint.yml` checks the README template and
Markdown; `security.yml` runs `pip-audit`; `codeql.yml` and
`scorecard.yml` scan; `release.yml` publishes a tag.
