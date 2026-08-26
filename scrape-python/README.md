# Data Engineering Example

A basic data engineering project covering web scraping, PostgreSQL, Docker, and GitHub.

## Contents

- Docker
- Web Scraping using BeautifulSoup (bs4)
- PostgreSQL
- Git & GitHub

## Project Structure

```text
uni-workshop/
├── README.md
├── scrape-python/
└── workshop_files/
```
## Docker

Navigate to the Python scraping project:

```bash
cd ~/uni-workshop/scrape-python
```

Build the Docker image and start the containers:

```bash
docker compose up --build
```

To run the containers in the background:

```bash
docker compose up --build -d
```

Check the running containers:

```bash
docker ps
```

Stop the containers:

```bash
docker compose down
```

To navigate into Python Container: 

```
docker compose run --rm python_service bash
```

To navigate into PosgreSQL Container: 

```bash
docker exec -it psql-db psql -U postgres
```

> [!NOTE]
> Might need to use `sudo` for navigation inside container or create a permission group of user.

## Web Scraping

The project uses Python and BeautifulSoup (`bs4`) to scrape and extract data from web pages.

The scraper runs inside the Docker environment along with the required Python dependencies.

## PostgreSQL

PostgreSQL is used as the database for storing the scraped data.

The PostgreSQL service is managed through Docker Compose, so there is no need to install PostgreSQL directly on the system.

