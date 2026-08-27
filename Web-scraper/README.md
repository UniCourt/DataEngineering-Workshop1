# Python Blog Scraper

Web-scrapes `https://blog.python.org/` to extract blog post titles, authors and
published dates, then stores them in a PostgreSQL database.

## Stack

- Python 3.10 (requests, BeautifulSoup, html5lib, psycopg2)
- Docker + Docker Compose
- PostgreSQL 14

## Usage

```bash
docker compose up --build
```

This builds the scraper image, starts a `psql-db` PostgreSQL container, scrapes
the blog, and inserts each blog post into the `blogs` table.

The database is exposed on host port `5434` (user `postgres`, password `123456`).

## Files

- `web_scraper.py` - main scraper that stores data in PostgreSQL
- `web_scraping_test.py` - minimal script that lists blog titles
- `Dockerfile` - container image for the scraper
- `docker-compose.yaml` - runs the scraper and a PostgreSQL service
- `requirements.txt` - Python dependencies
