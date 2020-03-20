pip.install:
	pip install -r requirements.txt

config.env:
	cp .env.sample .env

test:
	python -m unittest