# Contributing to bankstatementparser-writer-ofx

Thank you for your interest in `bankstatementparser-writer-ofx`, part of the
[bankstatementparser](https://github.com/sebastienrousseau/bankstatementparser)
suite. Participation is governed by the
[Code of Conduct](CODE_OF_CONDUCT.md); report vulnerabilities privately
as [`SECURITY.md`](SECURITY.md) describes, never in a public issue.

## Setup

You need Python 3.10 or later, [Poetry](https://python-poetry.org/)
and Git with commit signing configured.

```bash
git clone https://github.com/sebastienrousseau/bankstatementparser-writer-ofx.git
cd bankstatementparser-writer-ofx
poetry install
make check
```

## Workflow

1. Branch from `main` (the maintainer's release work happens on
   `feat/v<next-version>`).
2. Make the change, with a test that fails before it and passes after.
3. Run `make check`: ruff (lint and format), mypy `--strict`, the
   complexity baseline, Bandit, pytest with the 100% line and branch
   coverage floor, interrogate at 100% docstring coverage, and the
   examples.
4. Commit with a signature and a sign-off: `git commit -S -s`.
5. Open a pull request against `main`; the PR template lists what it
   needs.

## Standards

- **Commits** follow [Conventional Commits](https://www.conventionalcommits.org/):
  a header of at most 50 characters (`fix: ...`, `feat: ...`,
  `docs: ...`), and a body that says what changed and why.
- **Line length** is 79 characters; `ruff format` formats the code.
- **Types**: every public function is annotated; mypy runs in strict
  mode.
- **Docstrings** on every module, class and function (interrogate
  enforces 100%).
- **Complexity**: each function stays within cyclomatic 10, cognitive
  15, Halstead difficulty 30 and 60 lines (`make complexity`);
  `scripts/complexity_baseline.json` lists older offenders and may only
  shrink.
- **Dependencies** live in `poetry.lock`. After changing it, regenerate
  the hashed exports in `requirements/` with
  `scripts/export_locked_requirements.py` (CI fails when they drift).

## License

By contributing, you agree that your contributions are dual-licensed
under the [Apache License 2.0](LICENSE-APACHE) or the
[MIT License](LICENSE-MIT), at the user's option.
