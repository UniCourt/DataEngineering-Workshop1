# Workshop 1 — Web Scraper + PostgreSQL + Docker

Scrapes **[scrapethissite.com](https://www.scrapethissite.com)** and stores the results
in a PostgreSQL database, fully Dockerised with Docker Compose.

---

## Project Structure

```
workshop1/
├── Dockerfile               # Multi-stage image (builder + runtime)
├── docker-compose.yml       # Wires scraper + postgres together
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
│
├── src/
│   ├── main.py              # Entry point / orchestrator
│   ├── scraper.py           # BeautifulSoup scraping logic (2 scrapers)
│   ├── database.py          # psycopg2 connection, inserts, schema bootstrap
│   └── models.py            # Dataclasses (SandboxPage, HockeyTeam)
│
├── sql/
│   └── init.sql             # CREATE TABLE statements
│
└── logs/                    # scraper.log written here at runtime
```

---

## What Gets Scraped

| Target URL | Table | Records |
|---|---|---|
| `/pages/` | `sandbox_pages` | ~5 sandbox pages (title, URL, description) |
| `/pages/forms/` (all pages) | `hockey_teams` | ~1,200 NHL season stats rows |

A third table `scrape_runs` logs every run with its status and row count.

---

## Quick Start

### 1. Prerequisites
- Docker ≥ 24
- Docker Compose v2 (`docker compose` or `docker-compose`)

### 2. Clone & configure
```bash
cp .env.example .env
# edit .env if you want different credentials
```

### 3. Build & run
```bash
docker compose up --build
```

Docker will:
1. Pull `postgres:15-alpine` and start Postgres
2. Build the `python:3.11-slim` scraper image
3. Wait for Postgres to pass its health-check
4. Run the scraper — logs stream to your terminal and to `./logs/scraper.log`

### 4. Inspect the data

While containers are running (or after, if you left the db service up):

```bash
# Open a psql shell inside the DB container
docker exec -it workshop1_db psql -U scraper_user -d scraper_db

# Then inside psql:
SELECT * FROM sandbox_pages;
SELECT * FROM hockey_teams LIMIT 20;
SELECT * FROM scrape_runs;
\q
```

### 5. Re-run the scraper
```bash
docker compose run --rm scraper
```

Duplicate rows are silently skipped (`ON CONFLICT DO NOTHING`), so re-running is safe.

---

## Running Locally (without Docker)

```bash
# 1. Create a virtual environment
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Export DB connection vars (point at a local Postgres)
export DB_HOST=localhost DB_PORT=5432
export DB_NAME=scraper_db DB_USER=scraper_user DB_PASSWORD=scraper_pass

# 4. Create the DB manually, then run
psql -U postgres -c "CREATE DATABASE scraper_db;"
psql -U postgres -c "CREATE USER scraper_user WITH PASSWORD 'scraper_pass';"
psql -U postgres -c "GRANT ALL ON DATABASE scraper_db TO scraper_user;"

PYTHONPATH=src python src/main.py
```

---

## Key Design Decisions

| Decision | Why |
|---|---|
| `psycopg2` (no ORM) | SQL stays visible — easier to learn and debug in a workshop |
| `ON CONFLICT DO NOTHING` | Idempotent — safe to re-run without cleaning the DB first |
| Multi-stage Dockerfile | Final image has no build tools; ~30% smaller |
| Health-check `depends_on` | Scraper only starts after Postgres is truly ready |
| `scrape_runs` audit table | See when each run happened and how many rows were saved |
| Exponential-backoff retry | Transient network issues don't crash the whole run |
