.PHONY: all \
		setup \
		run
venv/bin/activate: ## alias for virtual environment
	python -m venv venv
setup: venv/bin/activate ## project setup
	. venv/bin/activate; pip3 install -r requirements.txt
run: venv/bin/activate ## Run
	black job1