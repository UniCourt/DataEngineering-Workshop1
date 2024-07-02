FROM python:3.10.2-alpine3.15
# Create directories  
RUN mkdir -p /root/workspace/src
COPY ./python_web_scrape.py  /root/workspace/src
# Switch to project directory
WORKDIR /root/workspace/src
# Install required packages
RUN pip install --upgrade pip
RUN pip install requests bs4 html5lib psycopg2-binary
CMD ["python_web_scrape.py"]
ENTRYPOINT ["python"]


