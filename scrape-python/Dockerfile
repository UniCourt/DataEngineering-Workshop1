FROM python:3.10-slim
WORKDIR /app
COPY scrape-python.py .
RUN pip install --no-cache-dir \
    requests \
    beautifulsoup4 \
    html5lib \
    psycopg2-binary
CMD ["python", "scrape-python.py"]
