# Makefile for globomap-core-loader

# Pip executable path
PIP := $(shell which pip)

help:
	@echo
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean      to clean garbage left by builds and installation"
	@echo "  compile    to compile .py files (just to check for syntax errors)"
	@echo "  test       to execute all tests"
	@echo "  run        to run the loader app"
	@echo "  run_api    to run the loader api app"
	@echo

clean:
	@echo "Cleaning project ..."
	@rm -rf build dist *.egg-info
	@find . \( -name '*.pyc' -o  -name '__pycache__' -o -name '**/*.pyc' -o -name '*~' \) -delete

compile: clean
	@echo "Compiling source code..."
	@python -tt -m compileall .
	@pep8 --format=pylint --statistics loader driver api

tests: export ENV=test

tests: clean compile
	@python -m unittest discover -s tests/

setup: requirements.txt
	$(PIP) install -r $^

run_migrations:
	db-migrate --config=migrations/migrations.conf

run_loader: run_migrations
	@python run_loader.py $(module)

run_reset_loader:
	@python run_reset_loader.py

run_api: run_migrations
	@python run_api.py

deploy_api:
	@cp Procfile_api Procfile
	@tsuru app-deploy -a $(project) Procfile requirements.txt requirements.apt globomap_core_loader run_api.py
	@rm Procfile

deploy_loader:
	@cp Procfile_loader Procfile
	@tsuru app-deploy -a $(project) Procfile requirements.txt requirements.apt globomap_core_loader run_loader.py .python-version
	@rm Procfile

deploy_reset_loader:
	@cp Procfile_reset_loader Procfile
	@tsuru app-deploy -a $(project) Procfile requirements.txt requirements.apt globomap_core_loader run_reset_loader.py
	@rm Procfile

docker: ## Run a development web server
	@docker-compose build
	@docker-compose up -d
