FROM python:3.10-alpine

WORKDIR /app

COPY download_pdfs.py .

RUN pip install --upgrade pip
RUN pip install requests beautifulsoup4 html5lib

CMD ["python", "download_pdfs.py"]
