.PHONY: all setup run lint

venv/bin/activate:  ## Alias for virtual environment
	python -m venv venv

setup: venv/bin/activate  ## Project setup
	. venv/bin/activate; pip3 install -r requirements.txt

run: venv/bin/activate  ## Run
	black dags

lint: venv/bin/activate  ## Lint
	. venv/bin/activate; flake8 --exclude=./venv

all: setup run lint