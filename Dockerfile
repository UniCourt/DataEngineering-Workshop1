FROM python:3.10.2-alpine3.15
RUN mkdir -p /root/workspace/src
COPY ./web_scraping_sample.py /root/workspace/src
WORKDIR /root/workspace/src
RUN pip install --upgrade pip
RUN pip install requests bs4 html5lib pypdf
ENTRYPOINT ["python"]
CMD ["web_scraping_sample.py"]
