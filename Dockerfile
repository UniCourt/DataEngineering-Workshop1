FROM python:3.10-slim
WORKDIR /app
copy app.py /app/app.py
CMD ["python","app.py"]
