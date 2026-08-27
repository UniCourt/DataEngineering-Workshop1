FROM python:3.10.2-alpine3.15
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY web_scraping_sample.py schema.sql ./

CMD ["python", "web_scraping_sample.py"]
