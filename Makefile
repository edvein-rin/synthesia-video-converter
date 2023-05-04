help: ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@grep -Eh '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies.
	@poetry install

run: ## Run the project.
	@poetry run "run"

test: ## Test the project.
	@poetry run pytest

lint: ## Lint the project code.
	@echo "TODO linting"

format: ## Format the project code.
	@echo "TODO formatting"

build: ## Build the project.
	@poetry build -f sdist

release: ## Create a new tag for release.
	@echo "TODO release"

docs-start: ## Start documentation local web server.
	@echo "TODO docs-start"

docs-build: ## Build documentation.
	@echo "TODO docs-build"

docs-deploy: ## Deploy documentation build.
	@echo "TODO docs-deploy"

env-info: ## Display virtual environment and system information.
	@poetry env info
