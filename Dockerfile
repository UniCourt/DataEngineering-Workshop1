FROM python:3.10.2-alpine3.15

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY web_scraping_sample.py .

CMD ["python", "web_scraping_sample.py"]
