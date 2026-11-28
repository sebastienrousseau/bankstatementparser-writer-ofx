.PHONY: help install dev test lint format type-check security complexity doc-coverage examples bench fuzz docs demo audit requirements readme clean check

PYTHON ?= python3
POETRY ?= poetry
PKG := bankstatementparser_writer_ofx

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: ## Install runtime dependencies only
	$(POETRY) install --only main

dev: ## Install runtime and development dependencies
	$(POETRY) install

test: ## Run tests with the 100% line+branch coverage gate (pyproject.toml)
	$(POETRY) run pytest tests/

lint: ## Lint and check formatting with ruff
	$(POETRY) run ruff check .
	$(POETRY) run ruff format --check .

format: ## Fix lint findings and format with ruff
	$(POETRY) run ruff check --fix .
	$(POETRY) run ruff format .

type-check: ## Run mypy (strict) on the package and tests
	$(POETRY) run mypy $(PKG) tests

security: ## Run Bandit on the package
	$(POETRY) run bandit -r $(PKG) -c pyproject.toml

# Per-function ceilings (cyclomatic 10, cognitive 15, Halstead 30,
# 60 lines; 500 lines per file) against scripts/complexity_baseline.json,
# which may only shrink.
complexity: ## Enforce the complexity baseline
	$(PYTHON) scripts/check_complexity.py

doc-coverage: ## Enforce 100% docstring coverage
	$(POETRY) run interrogate -c pyproject.toml $(PKG)

examples: ## Run every example script
	@for f in examples/*.py; do echo "=== $$f ==="; $(POETRY) run python "$$f" || exit 1; done

bench: ## Run the benchmark (full sizes)
	$(POETRY) run python benches/bench_to_ofx.py

fuzz: ## Fuzz with Atheris for 60s (Linux x86_64, Python 3.12+)
	$(POETRY) install --with fuzz
	mkdir -p .fuzz-corpus
	$(POETRY) run python fuzz/fuzz_to_ofx.py .fuzz-corpus fuzz/corpus -max_total_time=60

docs: ## Build the user manual (mkdocs --strict) into site/
	$(POETRY) install --with docs
	NO_MKDOCS_2_WARNING=1 $(POETRY) run mkdocs build --strict

demo: ## Render the README demo GIF with VHS
	vhs .github/demo.tape

audit: ## pip-audit every locked requirement set
	@for f in runtime ci docs fuzz build sbom; do \
		$(POETRY) run pip-audit --require-hashes --disable-pip -r requirements/$$f.txt || exit 1; \
	done

requirements: ## Regenerate the hashed requirements/ exports from poetry.lock
	$(POETRY) run python scripts/export_locked_requirements.py --with dev --output requirements/ci.txt
	$(POETRY) run python scripts/export_locked_requirements.py --output requirements/runtime.txt
	$(POETRY) run python scripts/export_locked_requirements.py --with fuzz --output requirements/fuzz.txt
	$(POETRY) run python scripts/export_locked_requirements.py --with docs --output requirements/docs.txt

readme: ## Check README.md against the portfolio template
	scripts/readme-check.sh

clean: ## Remove build artefacts and caches
	rm -rf build/ dist/ site/ *.egg-info .pytest_cache/ .mypy_cache/ .ruff_cache/ htmlcov/ coverage.xml .coverage
	find . -type d -name __pycache__ -not -path './.venv/*' -exec rm -rf {} + 2>/dev/null || true

check: lint type-check security complexity test doc-coverage examples readme ## Run every local gate
