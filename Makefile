.PHONY: install virtualenv ipython clean tests pflake8

install:
	@echo "Installing for dev environment"
	@.venv/bin/python -m pip install -e ".[dev]"
	@.venv/bin/python -m pip install -e ".[test]"


virtualenv:
	@echo "Creating virtual environment..."
	@python3 -m venv .venv

ipython:
	@.venv/bin/ipython

lint:
	@.venv/bin/pflake8 dundie tests integration

fmt:
	@.venv/bin/isort dundie tests integration
	@.venv/bin/black dundie tests integration

test:
	@.venv/bin/pytest -s

watch:
	@ls **/*.py | entr pytest

clean:			  ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build
