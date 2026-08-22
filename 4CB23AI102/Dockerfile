FROM python:3.10.2-alpine3.15

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev

RUN mkdir -p /root/workspace/src
COPY ./ /root/workspace/src/
WORKDIR /root/workspace/src

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "scraper.py"]
