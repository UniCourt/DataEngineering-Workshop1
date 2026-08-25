FROM python:3.10.2-alpine3.15
# Create directories  
RUN mkdir -p /root/workspace/src
COPY ./requirements.txt  /root/workspace/src
COPY ./web_scraping_sample.py  /root/workspace/src
# Switch to project directory
WORKDIR /root/workspace/src
# Install required packages
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "web_scraping_sample.py"]
