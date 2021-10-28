
FROM python:3.9.6-alpine

ENV PYTHONUNBUFFERED=1

# TODO remove unnceserry packaegs for pillow
# install dependencies mostly for psycopg2 nad pillow
RUN apk update
RUN apk add \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    freetype-dev \
    fribidi-dev \
    harfbuzz-dev \
    jpeg-dev \
    lcms2-dev \
    openjpeg-dev \
    tcl-dev \
    tiff-dev \
    tk-dev \
    zlib-dev

# install packages for python
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# app directory
RUN mkdir /app
COPY ./ /app
WORKDIR /app

# create docker user and give him permissions
RUN adduser -D user
RUN chown -R user:user /app
RUN chmod -R 755 /app
USER user