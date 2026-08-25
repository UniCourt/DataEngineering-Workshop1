FROM python:3.10.2-alpine3.15
# Create directories  
RUN mkdir -p /root/workspace/src
# Switch to project directory
WORKDIR /root/workspace/src
