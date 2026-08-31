
# Blog Vacuum

Dockerized Python + PostgreSQL project that scrapes blog posts from [blog.python.org](https://blog.python.org) and stores them in the database.

## Stack
Python (`requests`, `BeautifulSoup`, `psycopg2`) + PostgreSQL + Docker Compose

## Run
```bash
docker compose up --build
```

## Check data
```bash
docker exec -it blog-vacuum-db-1 psql -U bloguser -d blogdb
```
```sql
SELECT * FROM posts;
```