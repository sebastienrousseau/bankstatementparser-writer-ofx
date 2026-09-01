# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Sphinx configuration for bankstatementparser-writer-ofx documentation."""

from __future__ import annotations

import importlib.metadata

project = "bankstatementparser-writer-ofx"
author = "Sebastien Rousseau"
copyright = "2023-2026, Sebastien Rousseau"

try:
    release = importlib.metadata.version("bankstatementparser-writer-ofx")
except importlib.metadata.PackageNotFoundError:
    release = "0.0.19"
version = ".".join(release.split(".")[:2])

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
html_theme = "furo"
html_title = f"bankstatementparser-writer-ofx {release}"
