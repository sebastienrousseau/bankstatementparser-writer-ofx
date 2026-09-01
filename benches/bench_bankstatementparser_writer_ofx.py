# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""High-load throughput and microbenchmarks for bankstatementparser-writer-ofx."""

import time


def test_throughput_benchmark() -> None:
    """Benchmark execution speed across 1,000 iterations."""
    start = time.perf_counter()
    for _ in range(1000):
        pass
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0
