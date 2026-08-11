FROM simple_python

RUN mkdir -p /root/workspace/src

COPY ./web_scraping_sample.py /root/workspace/src

WORKDIR /root/workspace/src

CMD ["sh"]


