pip.install:
	pip install -r requirements-dev.txt

config.data:
	mkdir data

config.env:
	cp .env.sample .env

config: config.data config.env

test:
	python -m unittest

flake8:
	flake8 .

stubgen:
	stubgen zoop_wrapper

mypy:
	mypy zoop_wrapper --ignore-missing-imports

coverage:
	coverage run -m unittest
	coverage report
	coverage xml

coverage.codacy: coverage
	python-codacy-coverage -r coverage.xml -t $$CODACY_PROJECT_TOKEN
docs.start:
	sphinx-quickstart

docs.autodoc:
	sphinx-apidoc -f -o docs/source .

docs.build:
	sphinx-build docs/source/ docs/
