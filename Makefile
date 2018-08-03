# Makefile for globomap-core-loader

# Pip executable path
PIP := $(shell which pip)

DOCKER_COMPOSE_FILE=$(shell make docker_file)

help:
	@echo
	@echo "Please use 'make <target>' where <target> is one of"
	@echo

	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## Clear *.pyc files, etc
	@echo "Cleaning project ..."
	@rm -rf build dist *.egg-info
	@find . \( -name '*.pyc' -o  -name '__pycache__' -o -name '**/*.pyc' -o -name '*~' \) -delete

compile: clean ## Compile source code
	@echo "Compiling source code..."
	@python3.6 -tt -m compileall globomap_core_loader
	@pycodestyle --format=pylint --statistics globomap_core_loader

tests: clean ## Run tests
	@echo "Running tests..."
	@export ENV=test
	@nosetests --verbose --rednose  --nocapture --cover-package=globomap_core_loader --with-coverage

tests_ci: clean ## Make tests to CI
	@echo "Running tests..."
	@export ENV=test
	@nosetests --verbose --rednose  --nocapture --cover-package=globomap_core_loader

run_version_control: ## Run version control
	@echo "Running version control..."
	@python3.6 migrations/manage.py version_control || true

run_migrations: run_version_control ## Run migrations
	@echo "Running migrations..."
	@python3.6 migrations/manage.py upgrade

run_loader: run_migrations ## Run the loader
	@echo "Running loader..."
	@python3.6 scripts/run_loader.py $(module)

run_reset_loader: ## Run the reset loader app
	@echo "Running reset loader..."
	@python3.6 scripts/run_reset_loader.py

run_api: run_migrations ## Run the loader API app
	@echo "Running api..."
	@python3.6 scripts/run_api.py

deploy_api: ## Deploy API
	@cp scripts/tsuru/Procfile_api Procfile
	@cp scripts/docker/requirements/requirements_api.txt requirements.txt
	@cp scripts/run_api.py run_api.py
	@tsuru app-deploy -a $(project) Procfile requirements.txt requirements.apt globomap_core_loader run_api.py .python-version || true
	@rm Procfile
	@rm requirements.txt
	@rm run_api.py

deploy_loader: ## Deploy Loader
	@cp scripts/tsuru/Procfile_loader Procfile
	@cp scripts/docker/requirements/requirements_loader.txt requirements.txt
	@cp scripts/run_loader.py run_loader.py
	@tsuru app-deploy -a $(project) Procfile requirements.txt requirements.apt globomap_core_loader run_loader.py .python-version || true
	@rm Procfile
	@rm requirements.txt
	@rm run_loader.py

deploy_reset_loader: ## Deploy reset loader
	@cp scripts/tsuru/Procfile_reset_loader Procfile
	@cp scripts/docker/requirements/requirements_reset_loader.txt requirements.txt
	@cp scripts/scheduler_reset_loader.py scheduler_reset_loader.py
	@tsuru app-deploy -a $(project) Procfile requirements.txt requirements.apt globomap_core_loader scheduler_reset_loader.py .python-version || true
	@rm Procfile
	@rm requirements.txt
	@rm scheduler_reset_loader.py

containers_start:## Start containers
	docker-compose --file $(DOCKER_COMPOSE_FILE) up -d

containers_build: ## Build containers
	docker-compose --file $(DOCKER_COMPOSE_FILE) build --no-cache

containers_stop: ## Stop containers
	docker-compose --file $(DOCKER_COMPOSE_FILE) stop

containers_clean: ## Destroy containers
	docker-compose --file $(DOCKER_COMPOSE_FILE) rm -s -v -f

dynamic_ports: ## Set ports to services
	./scripts/docker/ports.sh

docker_file:
	@if [[ -f "docker-compose-temp.yml" ]]; then \
		echo "docker-compose-temp.yml"; 		 \
	else                                         \
		echo "docker-compose.yml";               \
    fi
