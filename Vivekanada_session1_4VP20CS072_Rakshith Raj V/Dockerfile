FROM python:3.10.2-alpine3.15
# Create directories  
RUN mkdir -p /root/workspace/src
COPY ./hw.py  /root/workspace/src
# Switch to project directory
WORKDIR /root/workspace/src
# Install required packages
RUN pip install --upgrade pip
RUN pip install requests bs4 html5lib
