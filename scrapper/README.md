# Python Blog Scraper

This project scrapes blog posts from the Python Insider website and stores them in a PostgreSQL database.

## Features

- Scrapes blog titles
- Scrapes author names
- Scrapes published dates
- Scrapes blog content
- Scrapes blog URLs
- Stores the data in PostgreSQL
- Uses Docker and Docker Compose

## Project Structure

scrapper/
- scraper.py
- database.py
- requirements.txt
- Dockerfile
- docker-compose.yml
- README.md

## Technologies Used

- Python
- Requests
- BeautifulSoup
- PostgreSQL
- Docker
- Docker Compose

## Run the Project

docker compose up --build -d

Check containers:

docker ps -a

View scraper logs:

docker logs blog_scraper

## Check the Database

docker exec -it blog_postgres psql -U postgres -d blogs_db

Then run:

SELECT id, title, author, published_date FROM blogs;

To exit:

\q
