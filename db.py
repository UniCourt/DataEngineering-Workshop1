import os
from dotenv import load_dotenv

import psycopg2

load_dotenv()

DEFAULTS = {
    "DB_HOST": "psql-db",
    "DB_PORT": "5432",
    "DB_USER": "postgres",
    "DB_PASSWORD": "123456",
    "DB_NAME": "postgres",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS blog_posts (
    id         SERIAL PRIMARY KEY,
    heading    TEXT NOT NULL UNIQUE,
    author     TEXT,
    date       TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
"""


def get_connection():
    config = get_db_config()
    config["connect_timeout"] = 10
    return psycopg2.connect(**config)


def init_db(conn):
    with conn.cursor() as cur:
        cur.execute(SCHEMA)
    conn.commit()


def insert_posts(conn, rows):
    if not rows:
        return
    sql = (
        "INSERT INTO blog_posts (heading, author, date) "
        "VALUES (%s, %s, %s) "
        "ON CONFLICT (heading) DO UPDATE SET "
        "author = EXCLUDED.author, date = EXCLUDED.date"
    )
    with conn.cursor() as cur:
        cur.executemany(sql, rows)
    conn.commit()


def get_db_config():
    cfg = {}
    for key in ("DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME"):
        cfg[key] = os.getenv(key, DEFAULTS[key])
    return {
        "host": cfg["DB_HOST"],
        "port": cfg["DB_PORT"],
        "user": cfg["DB_USER"],
        "password": cfg["DB_PASSWORD"],
        "dbname": cfg["DB_NAME"],
    }
