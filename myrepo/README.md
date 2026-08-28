# Workshop 1 Homework — Python Blog Scraper

## Homework

This project scrapes blog posts from the Python Blog and stores the
scraped data in a PostgreSQL database.

The project is Dockerized using Docker Compose.

## Data Collected

For each blog post, the scraper stores:

- Title
- Author
- Published date
- URL
- Description

## Project Structure

```text
myrepo/
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── scraper.py
└── README.md
