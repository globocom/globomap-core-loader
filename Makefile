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
	@python3.6 -tt -m compileall .
	@pep8 --format=pylint --statistics loader driver api

tests: clean compile
	@python3.6 -m unittest discover -s tests/

run_migrations:
	@python3.6 migrations/manage.py upgrade

run_loader:
	@python3.6 run_loader.py $(module)

run_reset_loader:
	@python3.6 run_reset_loader.py

run_api:
	@python3.6 run_api.py

deploy_api:
	@cp scripts/tsuru/Procfile_api Procfile
	@cp scripts/docker/requirements/requirements_api.txt requirements.txt
	@tsuru app-deploy -a $(project) Procfile requirements.txt requirements.apt globomap_core_loader run_api.py
	@rm Procfile
	@rm requirements.txt

deploy_loader:
	@cp scripts/tsuru/Procfile_loader Procfile
	@cp scripts/docker/requirements/requirements_loader.txt requirements.txt
	@tsuru app-deploy -a $(project) Procfile requirements.txt requirements.apt globomap_core_loader run_loader.py .python-version
	@rm Procfile
	@rm requirements.txt

# deploy_reset_loader:
# 	@cp scripts/tsuru/Procfile_reset_loader Procfile
# 	@tsuru app-deploy -a $(project) Procfile requirements.txt requirements.apt globomap_core_loader run_reset_loader.py
# 	@rm Procfile

docker: ## Run a development web server
	@docker-compose build
	@docker-compose up -d
