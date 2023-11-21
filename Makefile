VENV_NAME?=.venv
PYTHON_VERSION?=3.11

venv-create:
	python$(PYTHON_VERSION) -m venv $(VENV_NAME)
	pip install poetry
	poetry install

venv-activate:
	. $(VENV_NAME)/bin/activate

venv-clean:
	rm -rf $(VENV_NAME)

source:
	source $(PWD)/.env.sh &&

run-local:
	source $(PWD)/.env.sh && \
	python -m src start-server

clean:
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	rm -rf build/ dist/ *.egg-info/

lint:
	poetry run black . && \
	poetry run isort .

ruff:
	poetry run ruff $(SRC) --fix .

pyright:
	poetry run pyright $(SRC) .

test:
	source $(PWD)/.env.sh && \
	poetry run pytest

coverage:
	coverage run --rcfile ./pyproject.toml -m pytest ./tests && \
	coverage report --fail-under 95
