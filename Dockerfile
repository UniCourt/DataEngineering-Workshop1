FROM python:3.9

WORKDIR /root/workspace

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY python_blog_scraper.py .

CMD ["python", "python_blog_scraper.py"]