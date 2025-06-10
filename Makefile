PWD := $(shell pwd)
PROJECTNAME := $(shell basename "$(PWD)")
PACKAGE := $(PROJECTNAME)
PYTHON := $(shell which python)
PIP := $(shell which pip)
PYV := $(shell $(PYTHON) -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)")
DATASTORAGE := $(PWD)/data-storage
CONFIGSTORAGE := $(PWD)/configs-storage

REQFILE_TOOLS := requirements-tools.txt

#### -include Makefile.include
include env.infra
export

help: ## Show this help
	@printf "\n\033[33m%s:\033[1m\n" 'Choose available commands run in "$(PROJECTNAME)"'
	@echo "======================================================"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[32m%-15s		\033[35;1m-- %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@printf "\033[33m%s\033[1m\n"
	@echo "======================================================"


envs: ## Display envs
	@echo "======================================================"
	@echo "CONFIGSTORAGE $(CONFIGSTORAGE)"
	@echo "REQFILE_TOOLS $(REQFILE_TOOLS)"
	@echo "DATASTORAGE $(DATASTORAGE)"
	@echo "PACKAGE $(PACKAGE)"
	@echo "PROJECTNAME $(PROJECTNAME)"
	@echo "PYTHON $(PYTHON)"
	@echo "PIP $(PIP)"
	@echo "PYV $(PYV)"
	@echo "PWD $(PWD)"
	@echo "======================================================"
	@cat /etc/os-release | grep PRETTY_NAME  && docker -v && docker-compose -v && git --version &&  make -v
	@echo "======================================================"


run-services: ## Start services on docker compose
	@DATA_STORAGE=$(DATASTORAGE) CONFIGS_STORAGE=$(CONFIGSTORAGE) docker compose --env-file env.infra -f docker-compose.services.yml up --build &

stop-services: ## Stop services on docker compose
	@DATA_STORAGE=$(DATASTORAGE) CONFIGS_STORAGE=$(CONFIGSTORAGE) docker compose --env-file env.infra -f docker-compose.services.yml down > /dev/null


run-infra: ## Start infra
	DATA_STORAGE=$(DATASTORAGE) CONFIGS_STORAGE=$(CONFIGSTORAGE) docker compose --env-file env.infra -f docker-compose.infra.yml up -d > /dev/null


install-requirements: ## Install requirements-tools
	@echo "======================================================"
	@echo "install REQFILE_TOOLS $(REQFILE_TOOLS) $(PYV)"
	@echo "======================================================"
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r $(REQFILE_TOOLS)
	@echo "======================================================"


clean: ## Clean sources
	@echo "======================================================"
	@echo clean $(PROJECTNAME)
	@echo $(find ./* -maxdepth 0 -name "*.pyc" -type f)
	echo $(find . -name ".DS_Store" -type f)
	@rm -fR __pycache__ venv "*.pyc"
	@find ./* -maxdepth 0 -name "*.pyc" -type f -delete
	@find ./* -name '*.py[cod]' -delete
	@find ./* -name '__pycache__' -delete
	find . -name '*.DS_Store' -delete



list: ## Makefile target list
	@echo "======================================================"
	@echo Makefile target list
	@echo "======================================================"
	@cat Makefile | grep "^[a-z]" | awk '{print $$1}' | sed "s/://g" | sort