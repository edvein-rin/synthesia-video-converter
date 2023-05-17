help: FORCE ## Show help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@grep -Eh '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

install: FORCE ## Install dependencies.
	@if ! poetry --version > /dev/null; then echo 'Install Poetry: https://python-poetry.org/'; exit 1; fi
	@poetry install

setup-pre-commit-hooks: FORCE ## Setup pre-commit hooks.
	@poetry run pre-commit install

run: FORCE ## Run CLI.
	@poetry run bash -c "python -m src ${video}"

dev: FORCE ## Run CLI in a dev mode.
	@poetry run bash -c "python -m src ${video} --debug"

# TODO separate build for binaries (Win, MacOS) and package (python module)
# https://pyinstaller.org/en/stable/usage.html#building-macos-app-bundles
build: FORCE ## Build binaries for different systems.
	@rm -rf ./dist
	@rm -rf ./build
	# UNIX
	@poetry build -f sdist
	@find ./dist -name "*.tar.gz" -exec tar -zxvf {} -C ./dist/ \; -exec rm -rf {} \;
	@find ./dist -name "src" -exec sh -c "mv '{}'/* '{}/..'" \;
	@find ./dist -name "src" -exec rm -rf {} +
	@mv ./dist/* ./dist/synthesia-video-converter
	# Windows
	@poetry run pyinstaller src/__main__.py --onefile --name synthesia-video-converter.exe

test: FORCE ## Test project.
	@poetry run pytest

lint: FORCE ## Lint project code.
	@echo "TODO linting"

format: FORCE ## Format project code.
	@echo "TODO formatting"

release: FORCE ## Create a new tag for release.
	@echo "TODO release"

docs-start: FORCE ## Start documentation local web server.
	@poetry run mkdocs serve

docs-build: FORCE ## Build documentation.
	@poetry run mkdocs build

docs-deploy: FORCE ## Deploy documentation build.
	@poetry run mkdocs gh-deploy

clean: FORCE ## Clean ignored files.
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build
	@rm -rf site
	@find ./ -name '*.pyc' -exec rm -f {} +
	@find ./ -name '*.spec' -exec rm -f {} +
	@find ./ -name '__pycache__' -exec rm -rf {} +
	@find ./ -name 'Thumbs.db' -exec rm -f {} +
	@find ./ -name '*~' -exec rm -f {} +

export-dependencies: FORCE ## Export dependencies into requirements.txt.
	@poetry export --without-hashes --format=requirements.txt > requirements.txt

env-info: FORCE ## Display virtual environment and system information.
	@poetry env info

# https://www.gnu.org/software/make/manual/html_node/Force-Targets.html#Force-Targets
FORCE:
