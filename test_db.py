import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="blogdb",
    user="postgres",
    password="password",
    port=5432
)

print("Connected to PostgreSQL!")

conn.close()
