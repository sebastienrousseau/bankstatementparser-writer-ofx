# Examples for bankstatementparser-writer-ofx

Runnable scripts, each run in CI (`for f in examples/*.py`) and by
`tests/test_regression_examples.py`.

- `01_basic_usage.py`: serialises two `Transaction` objects with
  `to_ofx` and prints the statement part of the OFX document.
- `02_advanced_workflow.py`: parses [`data/statement.csv`](data/statement.csv)
  with the core `bankstatementparser`, writes it with `write_ofx` to a
  temporary directory, and parses the OFX file back.
