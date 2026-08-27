# UniCourt Workshop 1 - Web Scraping and PostgreSQL

## Objective

Scrape blog data from the Python Blog website and store the scraped data in a PostgreSQL database. The complete application is Dockerized using Docker Compose.

## Technologies Used

- Python 3.12
- Requests
- BeautifulSoup
- PostgreSQL 17
- Docker
- Docker Compose

## Data Scraped

The scraper extracts:

- Blog title
- Author
- Publication date
- Blog URL

## Project Structure

```text
unicourt-homework/
├── scraper.py
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
└── README.md
