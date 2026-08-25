FROM python:3.10-alpine

WORKDIR /app

COPY scraper.py .

RUN pip install --upgrade pip
RUN pip install requests beautifulsoup4 psycopg2-binary

CMD ["python", "scraper.py"]
