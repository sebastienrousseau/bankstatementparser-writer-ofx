# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.0.x   | :white_check_mark: |

Fixes land on the latest `0.0.x` release; there are no back-ported
branches.

## Reporting a Vulnerability

If you discover a security vulnerability in `bankstatementparser-writer-ofx`, report it
privately: open a
[private security advisory](https://github.com/sebastienrousseau/bankstatementparser-writer-ofx/security/advisories/new)
on GitHub or email **<sebastian.rousseau@gmail.com>**. Do not open a
public issue.

Please include a description, steps to reproduce (a minimal input is
ideal, with account data redacted), the impact you see and any fix you
suggest.

## What this package does and does not protect

`bankstatementparser-writer-ofx` turns transactions you already hold
into OFX 1.02 text, and writes it to a path only when you call
`write_ofx`.

- **No network and no reads.** It opens no connection and reads no
  file; `write_ofx` writes UTF-8 text to the path you give, creating
  missing parent directories.
- **Escaping.** Every value taken from the records or the arguments
  has `&`, `<` and `>` escaped and newlines replaced, so record text
  cannot open or close an OFX element (dates and the currency were
  written raw before 0.0.36).
- **Amounts** that cannot be parsed, or that are NaN or infinite, are
  written as `0.00` rather than raising; check your input if a total
  matters.
- **Fuzzing.** `fuzz/fuzz_to_ofx.py` drives `to_ofx` with Atheris in CI
  and fails on any exception, a lost record, a malformed amount or
  markup in an element value.

## Continuous checks

CodeQL, Bandit, `pip-audit` against the locked dependency sets, and the
Atheris fuzz target run on every pull request; OpenSSF Scorecard runs
weekly and on every push to `main`.
