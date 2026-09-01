# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Concurrency and stress tests for OFX writer."""

import time
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

from bankstatementparser.transaction_models import Transaction

from bankstatementparser_writer_ofx import to_ofx


def test_ofx_writer_concurrency() -> None:
    """Verify OFX export throughput under concurrent execution."""
    txns = [
        Transaction(
            account_id="ACC1",
            amount=Decimal("123.45"),
            currency="EUR",
            description="Client Payment",
            reference="REF001",
        )
        for _ in range(100)
    ]

    iterations = 500
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(to_ofx, txns) for _ in range(iterations)]
        results = [f.result() for f in futures]
    elapsed = time.perf_counter() - start

    assert len(results) == iterations
    for ofx_str in results:
        assert "<OFX>" in ofx_str
        assert "<TRNAMT>123.45" in ofx_str
    assert elapsed < 5.0
