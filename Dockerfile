FROM python:3.10.2-alpine3.15

# Install PostgreSQL
RUN apk update
RUN apk add --no-cache postgresql

# Create PostgreSQL runtime directory
RUN mkdir -p /run/postgresql/
RUN chown postgres:postgres /run/postgresql/

# Install dependencies required to build psycopg2
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    postgresql-dev

# Install Python requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Create application directory
RUN mkdir -p /root/workspace/src

# Copy Python scraper
COPY web_scraping_sample.py /root/workspace/src/

# Switch to project directory
WORKDIR /root/workspace/src
