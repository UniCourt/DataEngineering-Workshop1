FROM python:3.10-slim
COPY ./requirements.txt /root/workspace/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /root/workspace/requirements.txt
WORKDIR /app
