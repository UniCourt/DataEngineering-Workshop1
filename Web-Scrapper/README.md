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
- `web_scraping_test.py` - unittest suite to verify scraping and storage
- `Dockerfile` - container image for the scraper
- `docker-compose.yaml` - runs the scraper and a PostgreSQL service
- `requirements.txt` - Python dependencies

## Configuration

Database settings are configurable via environment variables (defaults shown):

| Variable       | Default     |
|----------------|-------------|
| `DB_HOST`      | `localhost` |
| `DB_PORT`      | `5432`      |
| `DB_USER`      | `postgres`  |
| `DB_PASSWORD`  | `123456`    |
| `DB_NAME`      | `postgres`  |
| `RETRY_ATTEMPTS` | `5`       |
| `RETRY_DELAY`  | `2`         |

When running under Docker Compose, `DB_HOST` is set to the `psql-db` service so
the scraper connects to the container database.
