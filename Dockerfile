FROM python:3.10.2-alpine3.15

RUN mkdir -p /root/workspace/src

COPY ./github_search.py /root/workspace/src

WORKDIR /root/workspace/src

RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev

RUN pip install --upgrade pip

RUN pip install requests bs4 html5lib psycopg2
