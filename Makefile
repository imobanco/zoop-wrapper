pip.install:
	pip install -r requirements.txt

config.data:
	mkdir data

config.env:
	cp .env.sample .env

config: config.data config.env

test:
	python -m unittest