FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir requests beautifulsoup4 html5lib psycopg2-binary

CMD ["python", "blog_scraper.py"]
