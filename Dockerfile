
FROM python:3.10.2-alpine3.15


WORKDIR /app


COPY requirements.txt .


RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps


COPY . .

CMD ["python", "python_blog_scraper.py"]
