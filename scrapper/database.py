import os
import psycopg2


def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "blogs_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        port=os.getenv("DB_PORT", "5432")
    )
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blogs (
            id SERIAL PRIMARY KEY,
            title TEXT,
            author TEXT,
            published_date TEXT,
            content TEXT,
            url TEXT UNIQUE
        )
    """)

    conn.commit()

    cursor.close()
    conn.close()


def insert_blog(blog):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO blogs
        (title, author, published_date, content, url)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (url) DO NOTHING
    """, (
        blog["title"],
        blog["author"],
        blog["date"],
        blog["content"],
        blog["url"]
    ))

    conn.commit()

    cursor.close()
    conn.close()
