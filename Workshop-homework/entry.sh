#!/bin/sh

echo "Starting Python Blog Scraper..."

echo "Waiting for PostgreSQL..."

until python -c "import psycopg; psycopg.connect(host='psql-db', port=5432, dbname='demo', user='postgres', password='123456').close()" 2>/dev/null
do
    echo "PostgreSQL is not ready yet..."
    sleep 2
done

echo "PostgreSQL is ready!"

echo "Running scraper..."

if python -u scrapper.py; then
    echo "Scraper completed successfully."
else
    echo "Scraper failed."
    exit 1
fi
