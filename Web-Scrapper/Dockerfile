FROM python:3.10.2-alpine3.15
RUN mkdir -p /root/workspace/src
COPY requirements.txt /root/workspace/src/
WORKDIR /root/workspace/src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY web_scraper.py /root/workspace/src/
CMD ["python", "web_scraper.py"]