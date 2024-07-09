# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files into the container
COPY web_scraping.py /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir requests bs4 psycopg2-binary

# Run the Python script when the container launches
CMD ["python", "./web_scraping.py"]
