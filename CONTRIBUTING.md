# Contribua

## Clone o projeto repositório
```shell script
git clone https://github.com/imobanco/ZoopAPIWrapper.git
```

## Setup env & data folder
run command to config `.env` file and `data` folder
```shell script
make config
```
Or
```shell script
make config.data
make config.env
```

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

### Running using Docker Compose (development):

First build:

`docker-compose build`

For development use: 

`docker-compose run zoopapiwrapper bash`

Note: the above command uses `run`, for development it is really handy.


## Bare python
requires python>=3.6

config virtual `env` for python with your python version
```shell script
python3.6 -m venv env
```

### Active env
on project folder run
```shell script
source env/bin/activate
```

### Install libs
on project folder and with env active

```shell script
make pip.install
```

### Running tests
on project folder and with env active

```shell script
make test
```