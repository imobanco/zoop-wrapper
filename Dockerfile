FROM python:3.8.2-buster

# If you do not know for what this variable is for see:
# https://stackoverflow.com/questions/45594707/what-is-pips-no-cache-dir-good-for
ENV PIP_NO_CACHE_DIR=false

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt
COPY requirements-dev.txt /requirements-dev.txt

# Note: If you need a specific version of pip use:
# pip install --upgrade pip==x.x.x
# For example: 19.2.2
# pip install --upgrade pip==19.2.2
#
# If you want to disable the pip version check see:
# https://stackoverflow.com/a/60270281
# ENV PIP_DISABLE_PIP_VERSION_CHECK=1
RUN pip install --upgrade pip \
&& pip install -r requirements-dev.txt
