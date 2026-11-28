<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

<p align="center">
  <img src="https://cloudcdn.pro/bankstatementparser/v1/logos/bankstatementparser.svg" alt="bankstatementparser-writer-ofx logo" width="128" />
</p>

<h1 align="center">bankstatementparser-writer-ofx</h1>

<p align="center">
  Writes bankstatementparser transactions as OFX 1.02 bank statements that accounting and personal-finance software can import.
</p>

<p align="center">
  <a href="https://github.com/sebastienrousseau/bankstatementparser-writer-ofx/actions"><img src="https://img.shields.io/github/actions/workflow/status/sebastienrousseau/bankstatementparser-writer-ofx/ci.yml?style=for-the-badge&logo=github" alt="Build" height="28" /></a>
  <a href="https://pypi.org/project/bankstatementparser-writer-ofx/"><img src="https://img.shields.io/pypi/v/bankstatementparser-writer-ofx?style=for-the-badge&color=fc8d62&logo=python" alt="Registry" height="28" /></a>
  <a href="https://sebastienrousseau.com/bankstatementparser-writer-ofx/"><img src="https://img.shields.io/badge/docs-user%20manual-0a7bbb?style=for-the-badge&labelColor=555555&logo=materialformkdocs" alt="Docs" height="28" /></a>
  <a href="https://scorecard.dev/viewer/?uri=github.com/sebastienrousseau/bankstatementparser-writer-ofx"><img src="https://img.shields.io/ossf-scorecard/github.com/sebastienrousseau/bankstatementparser-writer-ofx?style=for-the-badge&label=OpenSSF%20Scorecard&logo=openssf" alt="OpenSSF Scorecard" height="28" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0%20OR%20MIT-blue.svg?style=for-the-badge" alt="License: Apache-2.0 OR MIT" height="28" /></a>
  <a href="https://github.com/sebastienrousseau/bankstatementparser-writer-ofx/blob/main/docs/POLICIES.md"><img src="https://img.shields.io/badge/python-3.10%2B-93450a.svg?style=for-the-badge&logo=python" alt="Python 3.10+" height="28" /></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/sebastienrousseau/bankstatementparser-writer-ofx/main/.github/demo.gif" alt="A terminal printing the installed version, 0.0.37, then the two examples: two transactions written as OFX statement blocks, and a CSV statement converted to an OFX file and parsed back into four transactions" width="100%" />
</p>

---

## Contents

**Getting started**

- [Install](#install): PyPI, source
- [Requirements](#requirements): toolchain floor, platforms
- [Quick Start](#quick-start): convert a parsed statement to OFX

**The bankstatementparser-writer-ofx ecosystem**

- [The bankstatementparser-writer-ofx ecosystem](#the-bankstatementparser-writer-ofx-ecosystem): the core library, the loaders, writers and servers

**Library reference**

- [Capabilities at a glance](#capabilities-at-a-glance): the current surface by theme
- [Ecosystem comparison](#ecosystem-comparison): short matrix; full table at [`docs/COMPARISON.md`](docs/COMPARISON.md)
- [Benchmarks](#benchmarks): headline numbers; full table at [`docs/BENCHMARKS.md`](docs/BENCHMARKS.md)
- [Features](#features): the public API and field mapping
- [Configuration](#configuration): the writer's arguments
- [Examples](#examples): runnable example index

**Operational**

- [When not to use bankstatementparser-writer-ofx](#when-not-to-use-bankstatementparser-writer-ofx): limitations
- [Development](#development): make targets, fuzzing, CI
- [Security](#security): guarantees and compliance
- [Documentation](#documentation): all reference docs
- [Stability guarantees](#stability-guarantees): SemVer axis, output stability, minimum toolchain discipline
- [License](#license)

---

## Install

### As a Python library

```bash
pip install bankstatementparser-writer-ofx
```

That installs the writer, `bankstatementparser >= 0.0.36` and pandas.

| Channel | Command | Notes |
| :--- | :--- | :--- |
| PyPI | `pip install bankstatementparser-writer-ofx` | Pulls in `bankstatementparser >= 0.0.36` |
| Source | `git clone https://github.com/sebastienrousseau/bankstatementparser-writer-ofx && cd bankstatementparser-writer-ofx && poetry install` | For local development |

Verify the installation:

```sh
python -c "import bankstatementparser_writer_ofx as w; print(w.__version__)"
# -> 0.0.37
```

An isolated virtual environment keeps its dependencies apart:

```sh
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
python -m pip install -U bankstatementparser-writer-ofx
```

---

## Requirements

- **Python 3.10 or later.** CI tests CPython 3.10, 3.11, 3.12, 3.13 and 3.14 on Linux, macOS and Windows; [`docs/POLICIES.md`](docs/POLICIES.md) says when the floor moves.
- **[`bankstatementparser`](https://pypi.org/project/bankstatementparser/) 0.0.36 or later**, for the `Transaction` model and the parsers that feed the writer, and pandas, which it brings.

---

## Quick Start

```python
from bankstatementparser import create_parser

from bankstatementparser_writer_ofx import write_ofx

# 1. Parse a statement in any format the core supports
parser = create_parser("statement.csv")

# 2. Write it as an OFX 1.02 bank statement
write_ofx(
    parser,
    "statement.ofx",
    bank_id="123456789",
    account_id="987654321",
    currency="EUR",
)
```

`write_ofx` accepts the parser itself (it calls `parse()`), the DataFrame `parse()` returns, a list of `Transaction` objects or a list of dicts, and returns the `Path` it wrote. `to_ofx` takes the same arguments without the destination and returns the document as a string.

---

## The bankstatementparser-writer-ofx ecosystem

`bankstatementparser` is a modular suite whose packages ship one version together. This package is its OFX writer; the full table, with every loader, writer and server, is in [The suite](docs/suite.md).

| Component | Purpose | Use case |
| :--- | :--- | :--- |
| [`bankstatementparser`](https://github.com/sebastienrousseau/bankstatementparser) | The parser core: CAMT, pain.001, CSV, OFX, QFX, MT940 and PDF statements | Parsing statements from Python or the CLI |
| **`bankstatementparser-writer-ofx`** | Transactions to OFX 1.02 | Importing statements into accounting tools |
| Other writers | XLSX, QIF and SWIFT MT940/MT942 | Other export formats |
| Loaders | BAI2, MT942, CFONB, CAMT.054, SEPA and BACS | Formats beyond the core |
| [`bankstatementparser-transport-ebics`](https://github.com/sebastienrousseau/bankstatementparser-transport-ebics), [`bankstatementparser-mcp`](https://github.com/sebastienrousseau/bankstatementparser-mcp), [`bankstatementparser-lsp`](https://github.com/sebastienrousseau/bankstatementparser-lsp) | EBICS data, Model Context Protocol and Language Server Protocol | Bank downloads, AI agents and editors |

---

## Capabilities at a glance

| Area | Capability | Status |
| :--- | :--- | :--- |
| Input | `list[Transaction]`, `pandas.DataFrame`, `list[dict]`, or a core parser object | Shipped |
| OFX structure | `<SIGNONMSGSRSV1>`, `<BANKMSGSRSV1>`, `<STMTRS>`, `<BANKTRANLIST>` and `<LEDGERBAL>` | Shipped |
| Transactions | `<TRNTYPE>` (`CREDIT`, `DEBIT`), `<DTPOSTED>`, `<TRNAMT>`, `<FITID>`, `<NAME>`, `<MEMO>` | Shipped |
| Escaping | `&`, `<` and `>` in every value; newlines removed | Shipped |
| OFX 1.02 SGML | The format written | Shipped |
| OFX 2.x XML | Not written | Not implemented |

---

## Ecosystem comparison

The choice is between this one-call writer for parsed statements and a full OFX library. Every cell comes from this repository or the other project's PyPI description.

| Project | OFX 1.x | OFX 2.x | Writes from |
| :--- | :---: | :---: | :---: |
| **bankstatementparser-writer-ofx** | Yes (1.02) | No | `bankstatementparser` transactions |
| [`ofxtools`](https://pypi.org/project/ofxtools/) | Yes | Yes | Its own OFX object model |

See [`docs/COMPARISON.md`](docs/COMPARISON.md) for the evidence and complete matrix.

---

## Benchmarks

`benches/bench_to_ofx.py` times one `to_ofx` call for each input shape as the statement grows. Cost is linear: about 5 us per transaction from dicts, 12 us from `Transaction` objects and 20 us from a DataFrame.

| Scenario | Result | Environment |
| :--- | ---: | :--- |
| 1,000 `Transaction` objects | 11.4 ms | Apple M1 Pro, macOS 27.2.1, CPython 3.12.16 |
| 10,000 `Transaction` objects (1.4 MiB of OFX) | 116 ms | Apple M1 Pro, macOS 27.2.1, CPython 3.12.16 |
| 10,000-row DataFrame | 197 ms | Apple M1 Pro, macOS 27.2.1, CPython 3.12.16 |

See [`docs/BENCHMARKS.md`](docs/BENCHMARKS.md) for methodology and full results.

---

## Features

- `to_ofx(data, bank_id="123456789", account_id=None, account_type="CHECKING", currency="EUR") -> str`: serialises transactions to an OFX 1.02 document.
- `write_ofx(data, destination, bank_id="123456789", account_id=None, account_type="CHECKING", currency="EUR") -> Path`: writes that document to `destination` as UTF-8, creating missing parent directories.

Each record becomes one `<STMTTRN>`: `<TRNAMT>` from the amount (two decimals), `<TRNTYPE>` `CREDIT` for a positive amount and `DEBIT` otherwise, `<DTPOSTED>` from the date, `<FITID>` from the transaction ID or reference, `<NAME>` from the payee or description and `<MEMO>` from the memo or reference. `<DTSTART>` and `<DTEND>` span the record dates and `<BALAMT>` is the sum of the amounts. The [Usage](docs/usage.md) page has the full mapping and fallbacks.

---

## Configuration

There is no configuration file or environment variable; the writer's arguments are the configuration:

| Argument | Default | Meaning |
| :--- | :--- | :--- |
| `bank_id` | `"123456789"` | `<BANKID>` |
| `account_id` | `None` | `<ACCTID>`; when `None`, the first record's account, else `0000000000` |
| `account_type` | `"CHECKING"` | `<ACCTTYPE>`, e.g. `SAVINGS` or `CREDITLINE` |
| `currency` | `"EUR"` | `<CURDEF>`; while it is `EUR`, the last record's currency wins |

---

## Examples

[`examples/`](examples/) holds two runnable scripts, each run in CI:

| Example | Demonstrates |
| :--- | :--- |
| [`01_basic_usage.py`](examples/01_basic_usage.py) | Two `Transaction` objects written with `to_ofx` |
| [`02_advanced_workflow.py`](examples/02_advanced_workflow.py) | A CSV statement ([`examples/data/statement.csv`](examples/data/statement.csv)) converted to an OFX file with `write_ofx` and parsed back |

---

## When not to use bankstatementparser-writer-ofx

- **You need OFX 2.x (XML).** Only OFX 1.02 SGML is written.
- **Your names are not ASCII and your importer is strict.** The header declares `ENCODING:USASCII` and `CHARSET:1252`, but `write_ofx` writes UTF-8.
- **You need a bank-reported balance.** `<LEDGERBAL>` is the sum of the written transactions.
- **You need bad input reported.** An unparseable, NaN, infinite or out-of-range amount is written as `0.00` and a missing date as the current time, without an error.
- **You need transaction types beyond credit and debit** (`CHECK`, `FEE`, `PAYMENT` and the like).
- **You need to read OFX.** Use the core [`bankstatementparser`](https://pypi.org/project/bankstatementparser/), which parses OFX and QFX.

---

## Development

```bash
git clone https://github.com/sebastienrousseau/bankstatementparser-writer-ofx.git
cd bankstatementparser-writer-ofx
poetry install
make check
```

`make check` runs the local gates: `ruff` lint and format, `mypy --strict`, Bandit, the complexity baseline (`scripts/check_complexity.py`), `pytest` with a 100% line and branch coverage floor, `interrogate` at 100% docstring coverage, the examples and the README template check. Other targets: `make bench`, `make fuzz` (Atheris, 60 s, Linux x86_64 with Python 3.12+), `make docs` (the MkDocs manual, `--strict`), `make audit` (`pip-audit` on the locked sets) and `make demo` (re-renders the GIF above with VHS from `.github/demo.tape`). CI adds the OS by Python matrix, the fuzz job, CodeQL and the Docs Lint gates. [`CONTRIBUTING.md`](CONTRIBUTING.md) covers the workflow and commit rules.

---

## Security

- **No network and no reads.** The writer opens no connection and reads no file; `write_ofx` writes only to the path you give.
- **Escaping.** Every value from the records or the arguments has `&`, `<` and `>` escaped and newlines removed, so record text cannot open or close an OFX element.
- **Fuzzing.** `fuzz/fuzz_to_ofx.py` drives `to_ofx` with Atheris in CI and fails on any exception, a lost record, a malformed amount or markup in an element value. It found the unescaped dates and currency and the out-of-range amounts fixed in 0.0.36.
- **Supply chain.** Dependencies are locked in `poetry.lock`, CI installs hash-pinned exports of it, and `pip-audit`, Bandit and CodeQL run on every change. Releases publish to PyPI through OIDC trusted publishing and carry cosign signatures, SLSA provenance and SBOMs; every workflow action is pinned by commit SHA except the SLSA generator, which must be referenced by tag.

Report vulnerabilities according to [`SECURITY.md`](SECURITY.md).

---

## Documentation

- **User manual:** [sebastienrousseau.com/bankstatementparser-writer-ofx](https://sebastienrousseau.com/bankstatementparser-writer-ofx/), built from [`docs/`](docs/) with MkDocs
- **API reference:** [the manual's API page](https://sebastienrousseau.com/bankstatementparser-writer-ofx/api/), generated from the docstrings
- **Developer docs:** [`CONTRIBUTING.md`](CONTRIBUTING.md), [`ARCHITECTURE.md`](ARCHITECTURE.md), [`GOVERNANCE.md`](GOVERNANCE.md), [`SUPPORT.md`](SUPPORT.md)
- **The suite:** [`docs/suite.md`](docs/suite.md), with every `bankstatementparser` package
- **History:** [`CHANGELOG.md`](CHANGELOG.md)

---

## Stability guarantees

- **Versioning.** Releases stay on the `0.0.x` line and step by exactly `0.0.1`, in lockstep with the rest of the `bankstatementparser` suite. Under SemVer a `0.0.x` release may break anything; this project names each break in the CHANGELOG instead.
- **The breaking axis is the output**: the OFX the writer produces for a given input. A change to an element, its value or its fallback is called out in the CHANGELOG as breaking, even when no Python signature moves.
- **Python API.** `to_ofx` and `write_ofx` keep their names and arguments; names starting with `_` are internal.
- **Minimum toolchain.** Python 3.10 is the floor; it moves only in a release, for the whole suite at once, with the reason in the CHANGELOG ([`docs/POLICIES.md`](docs/POLICIES.md)).

---

## License

Dual-licensed under [Apache License, Version 2.0](LICENSE-APACHE) or [MIT](LICENSE-MIT), at your option (`SPDX-License-Identifier: Apache-2.0 OR MIT`). Any contribution submitted for inclusion in the work shall be dual-licensed as above, without additional terms or conditions.
