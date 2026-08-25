FROM python:3.10.2-alpine3.15

# Install system dependencies required by psycopg2 to compile against libpq
RUN apk add --no-cache gcc musl-dev postgresql-dev libpq

# Create directories
RUN mkdir -p /root/workspace/src
COPY ./web_scraping_sample.py /root/workspace/src

# Switch to project directory
WORKDIR /root/workspace/src

# Install required packages
# psycopg2-binary bundles libpq and avoids the segfault caused by psycopg[binary]
# on Alpine's musl libc. We use psycopg2 (source build) here for correctness with Alpine.
RUN pip install --upgrade pip
RUN pip install requests bs4 html5lib psycopg2-binary
