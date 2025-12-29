# -------------------------------
# Project meta
# -------------------------------
PROJECT	?= "adif-mcp"
PYTHON	?= python3

# Persona Variables
PERSONA ?= Primary
PROVIDERS := eqsl lotw qrz clublog

# Pull versions from pyproject.toml (Python 3.11+ for tomllib)
PY_PROJ_VERSION := $(shell $(PYTHON) -c "import tomllib;print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])" 2>/dev/null)
ADIF_SPEC_VERSION := $(shell $(PYTHON) -c "import tomllib;d=tomllib.load(open('pyproject.toml','rb'));print(d.get('tool',{}).get('adif',{}).get('spec_version','unknown'))" 2>/dev/null)

# Optional defaults printed in the help header (leave blank if N/A)
FROM    ?=
TO      ?=
DB      ?=
PORT    ?=

# -------------------------------
# Color Helpers
# -------------------------------
# Foreground colors
C_R='\033[01;31m'		# red
C_G='\033[01;32m'		# green
C_Y='\033[01;33m'		# yellow
C_C='\033[01;36m'		# cyan
C_NC='\033[0m'		  # no color


.PHONY: help docs-serve docs-build clean-docs clean-all pre-commit-install gate

# Default task: Show available commands
help: # Display
	@echo "MCP Hub Management"
	@echo "  docs-serve       - Start local MkDocs server"
	@echo "  docs-build       - Build static site locally (strict)"
	@echo "  pre-commit-install - Re-install local git hooks"
	@echo "  gate             - Run all pre-commit checks on all files"
	@echo "  clean-docs       - Remove site directory"
	@echo "  clean-all        - Remove site, .venv, and caches"

# --- Documentation ---
docs-serve:
	uv run mkdocs serve

docs-build:
	uv run mkdocs build --strict

# --- Gatekeeping & Linting ---
pre-commit-install:
	uv sync
	uv run pre-commit install

gate:
	uv run pre-commit run --all-files

# --- Cleanup ---
clean-docs:
	rm -rf site/

clean-all: clean-docs
	rm -rf .venv/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
