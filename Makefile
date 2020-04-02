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
	stubgen ZoopAPIWrapper

mypy:
	mypy -m ZoopAPIWrapper
