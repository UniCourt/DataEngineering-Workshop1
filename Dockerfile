FROM python:3.10-slim

RUN mkdir -p /root/workspace/src

COPY ./web_scraping_sample.py /root/workspace/src
COPY ./blog_scraper.py /root/workspace/src

WORKDIR /root/workspace/src

RUN pip install --upgrade pip
RUN pip install requests bs4 html5lib psycopg2-binary
