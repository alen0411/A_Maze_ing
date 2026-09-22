PYTHON := python3
MAIN := src/main.py
CONFIG ?= config.txt

MLX_PATH := $(CURDIR)/mlx
SRC_PATH := $(CURDIR)/src

PYTHONPATH := $(SRC_PATH):$(MLX_PATH)

# ---------------------------------------------------------
# Allow:
#   make run 80
# where 80 becomes SEED=80 in config.txt
# ---------------------------------------------------------

KNOWN_TARGETS := all install run debug clean lint lint-strict check-mlx
ARGS := $(filter-out $(KNOWN_TARGETS),$(MAKECMDGOALS))
SEED := $(firstword $(ARGS))

ifneq ($(SEED),)
$(SEED):
	@:
endif


.PHONY: all install run debug clean lint lint-strict check-mlx

all: run


# ---------------------------------------------------------
# Install dependencies
# ---------------------------------------------------------

install:
	$(PYTHON) -m pip install --user flake8 mypy


# ---------------------------------------------------------
# Check MiniLibX
# ---------------------------------------------------------

check-mlx:
	@PYTHONPATH="$(PYTHONPATH)" $(PYTHON) -c "from mlx import Mlx" \
		|| (echo "Error: MiniLibX could not be imported"; exit 1)
	@echo "MiniLibX OK"


# ---------------------------------------------------------
# Run
#
# make run
# make run 80
# ---------------------------------------------------------

run: check-mlx
	@if [ ! -f "$(CONFIG)" ]; then \
		echo "Error: configuration file '$(CONFIG)' not found"; \
		exit 1; \
	fi
	@if [ -n "$(SEED)" ]; then \
		if ! echo "$(SEED)" | grep -Eq '^[0-9]+$$'; then \
			echo "Error: seed must be an integer"; \
			exit 1; \
		fi; \
		if grep -q '^SEED=' "$(CONFIG)"; then \
			sed -i 's/^SEED=.*/SEED=$(SEED)/' "$(CONFIG)"; \
		else \
			echo "SEED=$(SEED)" >> "$(CONFIG)"; \
		fi; \
		echo "Config updated: SEED=$(SEED)"; \
	fi
	@echo "Using configuration:"
	@grep '^SEED=' "$(CONFIG)" || echo "SEED=42 (default)"
	PYTHONPATH="$(PYTHONPATH)" $(PYTHON) $(MAIN) $(CONFIG)


# ---------------------------------------------------------
# Debug
# ---------------------------------------------------------

debug: check-mlx
	@if [ ! -f "$(CONFIG)" ]; then \
		echo "Error: configuration file '$(CONFIG)' not found"; \
		exit 1; \
	fi
	@if [ -n "$(SEED)" ]; then \
		if ! echo "$(SEED)" | grep -Eq '^[0-9]+$$'; then \
			echo "Error: seed must be an integer"; \
			exit 1; \
		fi; \
		if grep -q '^SEED=' "$(CONFIG)"; then \
			sed -i 's/^SEED=.*/SEED=$(SEED)/' "$(CONFIG)"; \
		else \
			echo "SEED=$(SEED)" >> "$(CONFIG)"; \
		fi; \
	fi
	PYTHONPATH="$(PYTHONPATH)" $(PYTHON) -m pdb $(MAIN) $(CONFIG)


# ---------------------------------------------------------
# Clean
# ---------------------------------------------------------

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "Clean complete"


# ---------------------------------------------------------
# Mandatory lint
# ---------------------------------------------------------

lint:
	flake8 .
	mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs


# ---------------------------------------------------------
# Optional strict lint
# ---------------------------------------------------------

lint-strict:
	flake8 .
	mypy . --strict