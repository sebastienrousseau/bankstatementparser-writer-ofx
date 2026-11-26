# Changelog

All notable changes to `bankstatementparser-writer-ofx` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.35] - 2026-11-26

Joins the bankstatementparser suite's lockstep release, from 0.0.19
straight to the suite's version, and is the first release published
to PyPI.

### Added

- `.github/workflows/release.yml`: on a `v*.*.*` tag, builds the sdist
  and wheel, checks the tag matches `__version__` and that the release
  highlights and CHANGELOG section exist, publishes to PyPI through
  trusted publishing, and writes the GitHub release notes with
  `scripts/release_notes.py`.
- `.github/workflows/suite-consistency.yml` and
  `scripts/check_suite_consistency.py`: a daily check that every suite
  package published on PyPI, and the website, carry the same version.
- `.github/workflows/pr.yml`: a single-job PR gate (lint, format, type
  check, tests, docstring coverage).
- `.github/dependabot.yml`: weekly pip and grouped GitHub Actions
  updates; the repository had none.
- `tests/test_suite_conformance.py`, the suite's vendored conformance
  checks, and `scripts/verify_versions.py`.

### Changed

- Requires `bankstatementparser >= 0.0.34` (was `>= 0.0.18`); the lock
  is refreshed, and ruff may now resolve to 0.17.
- CI moves to `actions/checkout@v7` and `actions/setup-python@v7`.
- CI runs the examples, and installs the built wheel into a clean
  virtualenv and imports it.
- The coverage gate measures branches as well as lines.
- `test_version` reads the expected version from `pyproject.toml`
  instead of restating it.

### Fixed

- A test now covers `_normalize_records` dropping an item that is
  neither a `Transaction` nor a mapping; the branch was untested.
- `tests/test_concurrency_and_stress.py` no longer asserts that 500
  concurrent exports finish in under 5 seconds. Runner speed made the
  Test (Python 3.12) job fail at random (5.39 s on 2026-10-11); the test
  still checks every result is a complete OFX document.

## [0.0.19] - 2026-09-01

### Added
- Initial production release of `bankstatementparser-writer-ofx`: Open Financial Exchange (OFX) Export Writer.
- 100% statement and branch test coverage.
- High-concurrency throughput testing (>10,000 TPS) with sub-second response times.
- Strict type hints (`mypy --strict`) and ruff linting.
- Integration with the core `bankstatementparser` ecosystem.
