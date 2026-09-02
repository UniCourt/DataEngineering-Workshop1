FROM python:3.12
WORKDIR /app
COPY blog.py .
RUN pip install requests beautifulsoup4 psycopg2-binary
CMD ["python", "blog.py"]



