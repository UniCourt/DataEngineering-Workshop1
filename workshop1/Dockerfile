# Use a small, official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first (better Docker layer caching:
# dependencies only get reinstalled if requirements.txt changes)
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code
COPY app/ .

# Command that runs when the container starts
CMD ["python", "scraper.py"]
