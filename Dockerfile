	
FROM python:3.10.2-alpine3.15

RUN mkdir -p /root/unicourt/test

RUN apk update
     RUN apk add postgresql
     RUN apk add postgresql-dev gcc python3-dev musl-dev
     
RUN pip install --upgrade pip
RUN pip install requests 
RUN pip install bs4 
RUN pip install html5lib 
RUN pip install psycopg2



COPY ./hi.py /root/unicourt/test
WORKDIR /root/unicourt/test

CMD ["hi.py"]
ENTRYPOINT ["python"]
