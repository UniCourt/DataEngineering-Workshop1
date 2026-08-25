FROM python:3.10-slim

WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Default command
CMD ["python", "scrap.py"]
