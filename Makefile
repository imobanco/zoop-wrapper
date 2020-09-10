pip.install:
	pip install -r requirements-dev.txt

pip.install.build:
	pip install -r requirements-build.txt

config.env:
	cp .env.sample .env

test:
	python -m unittest $(args)

fmt:
	black .

fmt.check: mypy
	black --check .
	flake8

stubgen:
	stubgen zoop_wrapper

mypy:
	mypy zoop_wrapper --ignore-missing-imports

coverage:
	coverage run -m unittest
	coverage report
	coverage xml

docs.start:
	sphinx-quickstart

docs.autodoc:
	sphinx-apidoc --force --output-dir docs/ .

docs.build:
	sphinx-build docs/ docs/build/
	touch docs/build/.nojekyll

package.build:
	python setup.py sdist bdist_wheel