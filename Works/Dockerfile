FROM python:3.10.2-alpine3.15

# Install system dependencies for build and postgres client
RUN apk update && apk add --no-cache postgresql-dev gcc musl-dev libpq

# Create directories  
RUN mkdir -p /root/workspace/src

# Copy the script
COPY ./p1.py /root/workspace/src/p1.py

# Switch to project directory
WORKDIR /root/workspace/src

# Install required packages
RUN pip install --upgrade pip
RUN pip install requests bs4 html5lib psycopg2-binary
