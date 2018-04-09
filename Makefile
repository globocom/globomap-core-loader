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
	@python3.6 -tt -m compileall globomap_core_loader
	@pycodestyle --format=pylint --statistics globomap_core_loader

test: clean
	@echo "Running tests..."
	@nosetests --verbose --rednose  --nocapture --cover-package=globomap_core_loader --with-coverage

run_migrations:
	@echo "Running migrations..."
	@python3.6 migrations/manage.py upgrade

run_loader:
	@echo "Running loader..."
	@python3.6 scripts/run_loader.py $(module)

run_reset_loader:
	@python3.6 scripts/run_reset_loader.py

run_api: run_migrations
	@echo "Running api..."
	@python3.6 scripts/run_api.py

deploy_api:
	@cp scripts/tsuru/Procfile_api Procfile
	@cp scripts/docker/requirements/requirements_api.txt requirements.txt
	@cp scripts/run_loader.py run_api.py
	@tsuru app-deploy -a $(project) Procfile requirements.txt requirements.apt globomap_core_loader run_api.py .python-version
	@rm Procfile
	@rm requirements.txt
	@rm run_api.py

deploy_loader:
	@cp scripts/tsuru/Procfile_loader Procfile
	@cp scripts/docker/requirements/requirements_loader.txt requirements.txt
	@cp scripts/run_loader.py run_loader.py
	@tsuru app-deploy -a $(project) Procfile requirements.txt requirements.apt globomap_core_loader run_loader.py .python-version
	@rm Procfile
	@rm requirements.txt
	@rm run_loader.py

# deploy_reset_loader:
# 	@cp scripts/tsuru/Procfile_reset_loader Procfile
# 	@tsuru app-deploy -a $(project) Procfile requirements.txt requirements.apt globomap_core_loader run_reset_loader.py
# 	@rm Procfile

docker: ## Run a development web server
	@docker-compose build
	@docker-compose up -d
