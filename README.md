# ZoopAPIWrapper


## Docker + docker-compose

Install [docker-ce](https://docs.docker.com/install/) and 
[docker-compose](https://docs.docker.com/compose/install/) from each documentation.


### Running using Docker (development):

First build a image named `zoopapiwrapper`.

`docker build --tag zoopapiwrapper .`

Running in development:
```
docker run -it \
--rm \
--env-file .env \
--volume "$(pwd)":/code \
--workdir /code \
zoopapiwrapper \
bash
```

## Running using Docker Compose (development):

First build:

`docker-compose build`

For development use: 

`docker-compose run zoopapiwrapper bash`

Note: the above command uses `run`, for development it is really handy.


## Running tests

`python -m unittest discover`

### Install for local development

`pip install --editable .`

`python -c "import ZoopAPIWrapper"`