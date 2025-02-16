.PHONY: venv install lint format clean run

venv:
	python -m venv .venv

install: venv
	python -m pip install -e ".[dev]"

lint:
	ruff check .
	mypy .

format:
	ruff format .
	ruff check --fix .

clean:
	rm -rf .mypy_cache .ruff_cache dist build __pycache__
	rm -rf .venv

run:
	reversi
