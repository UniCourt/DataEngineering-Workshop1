FROM python:3.10.2-alpine3.15

# Install build deps needed for psycopg2
RUN apk add --no-cache gcc musl-dev postgresql-dev

# Create working directory
RUN mkdir -p /root/workspace/src
WORKDIR /root/workspace/src

# Install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

CMD ["python", "main.py"]