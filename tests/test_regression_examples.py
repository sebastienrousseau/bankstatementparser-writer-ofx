# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Automated regression tests ensuring all examples execute cleanly."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_all_examples_execute() -> None:
    """Execute all python scripts in examples/ directory."""
    examples_dir = Path(__file__).resolve().parent.parent / "examples"
    example_files = sorted(examples_dir.glob("*.py"))

    assert len(example_files) >= 2
    for example_file in example_files:
        res = subprocess.run(
            [sys.executable, str(example_file)], capture_output=True, text=True
        )
        assert res.returncode == 0, (
            f"Example {example_file.name} failed: {res.stderr}"
        )
