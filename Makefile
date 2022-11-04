install: ## [Local development] Upgrade pip, install requirements, install package.
	python3 -m pip install -U pip
	python3 -m pip install -e .

install-dev: ## [Local development] Install test requirements
	python3 -m pip install -r requirements-test.txt

lint: ## [Local development] Run mypy, pylint and black
	python3 -m mypy audio2dataset
	python3 -m pylint audio2dataset
	python3 -m black --check -l 120 audio2dataset

black: ## [Local development] Auto-format python3 code using black
	python3 -m black -l 120 .

build-pex:
	python3 -m venv .pexing
	. .pexing/bin/activate && python3 -m pip install -U pip && python3 -m pip install pex
	. .pexing/bin/activate && python3 -m pex setuptools . -o python3_template.pex -v
	rm -rf .pexing

test: ## [Local development] Run unit tests
	python3 -m pytest -x -s -v tests

.PHONY: help

help: # Run `make help` to get help on the make commands
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'