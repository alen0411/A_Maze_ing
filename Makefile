PYTHON := python3
MAIN := a_maze_ing.py
CONFIG ?= config.txt

MLX_PATH := $(CURDIR)/mlx
SRC_PATH := $(CURDIR)/src

PYTHONPATH := $(SRC_PATH):$(MLX_PATH)

.PHONY: install run debug clean lint lint-strict

install:
	$(PYTHON) -m pip install --user flake8 mypy

run:
	PYTHONPATH="$(PYTHONPATH)" $(PYTHON) $(MAIN) $(CONFIG)

debug:
	PYTHONPATH="$(PYTHONPATH)" $(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

lint:
	flake8 .
	mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs
