.PHONY: venv install lint format clean run build

venv:
	python -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip

install: venv
	. .venv/bin/activate && python -m pip install -e ".[dev]"

lint:
	ruff check .
	mypy .

format:
	ruff format .
	ruff check --fix .

clean:
	rm -rf .mypy_cache .ruff_cache dist build __pycache__
	rm -rf .venv
	rm -rf *.egg-info **/*.egg-info
	rm -f reversi.spec

run:
	reversi

build:
	python -m build
	pyinstaller \
		--name reversi \
		--onefile \
		--windowed \
		--clean \
		--noconfirm \
		--distpath dist/exe \
		--collect-all pygame \
		--add-binary '/opt/homebrew/opt/gettext/lib/libintl.8.dylib:pygame/.dylibs/' \
		src/main.py
