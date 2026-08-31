# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Open Financial Exchange (OFX) Writer for bankstatementparser."""

from __future__ import annotations

from .writer import to_ofx, write_ofx

__version__ = "0.0.1"
__all__ = ["__version__", "to_ofx", "write_ofx"]
