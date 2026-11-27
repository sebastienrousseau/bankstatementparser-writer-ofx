# Benchmarks

`benches/bench_to_ofx.py` measures one `to_ofx` call as the statement
grows, for each input shape the writer accepts: a list of `Transaction`
objects, a pandas DataFrame and a list of dicts. Each figure is the best
of five runs after one warm-up. Nothing asserts a threshold: wall-clock
is not comparable between machines. CI runs
`python benches/bench_to_ofx.py --quick` on every operating system and
Python in the test matrix so the benchmark keeps running against the
current API.

## Results

Run with `poetry run python benches/bench_to_ofx.py` on 2026-11-27:
Apple M1 Pro, macOS 27.2.1, CPython 3.12.16,
bankstatementparser-writer-ofx 0.0.36 with bankstatementparser 0.0.35.

| Transactions | OFX KiB | Transactions ms | DataFrame ms | Dicts ms |
| ---: | ---: | ---: | ---: | ---: |
| 10 | 2.1 | 0.13 | 0.24 | 0.06 |
| 100 | 14.8 | 1.23 | 2.01 | 0.50 |
| 1,000 | 143.1 | 11.39 | 19.50 | 4.96 |
| 10,000 | 1,435.1 | 115.56 | 196.85 | 50.00 |

Cost is linear in every shape: per transaction it stays within 10% to
20% of the 10-record figure up to 10,000 records (about 5 us for dicts,
12 us for `Transaction` objects and 20 us for a DataFrame, whose rows
are converted to dicts first). A 10,000-transaction export takes about
a fifth of a second.

Reproduce with `python benches/bench_to_ofx.py` (add `--json` for
machine-readable output).
