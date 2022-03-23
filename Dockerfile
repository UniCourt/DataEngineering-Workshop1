FROM python:3.10.2-alpine3.15
# Install Postgres
RUN apk update
RUN apk add postgresql
RUN chown postgres:postgres /run/postgresql/
# Create directories
RUN mkdir -p /root/workspace/src
# Mount your local file
COPY ./web_scraping_sample.py /root/workspace/src
# Switch to project directory
WORKDIR /root/workspace/src