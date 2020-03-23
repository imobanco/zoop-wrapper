pip.install:
	pip install -r requirements.txt

config.env:
	cp .env.sample .env
	mkdir data

test:
	python -m unittest