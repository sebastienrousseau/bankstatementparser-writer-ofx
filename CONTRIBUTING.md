# Contributing to bankstatementparser-writer-ofx

Thank you for your interest in contributing to `bankstatementparser-writer-ofx`!

## Code of Conduct
We are committed to providing a friendly, safe, and welcoming environment for all contributors.

## Development Workflow
1. Fork and clone the repository.
2. Install dependencies:
   ```bash
   poetry install --all-extras
   poetry run pre-commit install
   ```
3. Ensure all tests and quality gates pass:
   ```bash
   poetry run pytest
   poetry run ruff check .
   poetry run ruff format --check .
   poetry run mypy .
   poetry run interrogate -v
   ```
4. Submit a Pull Request targeting `main`.
