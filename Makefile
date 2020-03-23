pip.install:
	pip install -r requirements-dev.txt

config.env:
	cp .env.sample .env
	mkdir data

test:
	python -m unittest