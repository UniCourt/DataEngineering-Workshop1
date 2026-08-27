FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies FIRST so Docker can cache this layer
# and it only reinstalls when requirements.txt actually changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the source code.
COPY . .

CMD ["python", "web_scraping_sample.py"]
