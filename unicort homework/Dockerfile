FROM python:3.10.2-alpine3.15
COPY . .
# Install Postgres
RUN apk update
RUN apk add postgresql
RUN chown postgres:postgres /run/postgresql/
# Install requirements
COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
# For psycopg2
RUN apk add --virtual postgresql-deps libpq-dev
# Create directories
RUN mkdir -p /root/workspace/src
# Mount your local file
COPY ./web_scraping_sample.py /root/workspace/src
# Switch to project directory
WORKDIR /root/workspace/src