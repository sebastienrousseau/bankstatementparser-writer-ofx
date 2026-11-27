<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# bankstatementparser-writer-ofx Governance

How bankstatementparser-writer-ofx is run and how decisions are made.

## Scope

bankstatementparser-writer-ofx is one package of the
[`bankstatementparser`](https://github.com/sebastienrousseau/bankstatementparser)
suite: it writes the suite's parsed transactions as OFX 1.02 bank statements. Changes are weighed against that scope: correctness,
security and clarity over feature breadth.

## Roles

| Role | Who | Can |
| :--- | :--- | :--- |
| **Maintainer** | Sebastien Rousseau | Merge pull requests, cut releases, triage, set direction |
| **Contributor** | Anyone with a merged pull request | Propose changes, review, discuss |
| **User** | Everyone | File issues, ask questions, request features |

## Decisions

- **Fixes, docs, tests and additive features** within scope proceed by
  pull request: if CI is green and the maintainer agrees, it is merged.
- **Breaking changes, new public API and new dependencies** start as an
  issue, so the reasoning is recorded before code is written.
- Every change passes the same gates whoever wrote it: 100% line and
  branch coverage, 100% docstring coverage, mypy `--strict`, ruff,
  Bandit, the complexity baseline, CodeQL and `pip-audit`, all enforced
  in CI.

## Releases

The suite ships one version across every package, stepping by `0.0.1`.
A release is a signed tag `v<version>`; `.github/workflows/release.yml`
publishes it to PyPI through trusted publishing and attaches signatures,
SLSA provenance and SBOMs to the GitHub release.

## Sustainability

The project has one maintainer. What keeps it legible to the next one:
[`ARCHITECTURE.md`](ARCHITECTURE.md) maps the code, CI enforces the
quality bar, and every example runs in CI. Anyone who wants to help
maintain it can start by reviewing pull requests and triaging issues.

## Conduct and security

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).
Report vulnerabilities privately as [`SECURITY.md`](SECURITY.md)
describes, never in a public issue.
