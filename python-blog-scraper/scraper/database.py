import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def insert_posts(posts):

    connection = get_connection()

    inserted_count = 0

    try:
        with connection.cursor() as cursor:

            for post in posts:

                cursor.execute(
                    """
                    INSERT INTO blog_posts (
                        title,
                        author,
                        published_date,
                        summary,
                        url,
                        scraped_at
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    ON CONFLICT (url) DO NOTHING
                    """,
                    (
                        post["title"],
                        post["author"],
                        post["published_date"],
                        post["summary"],
                        post["url"],
                        post["scraped_at"]
                    )
                )

                inserted_count += cursor.rowcount

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return inserted_count

def get_posts():

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    author,
                    published_date,
                    summary,
                    url,
                    scraped_at
                FROM blog_posts
                ORDER BY published_date DESC
                """
            )

            rows = cursor.fetchall()

            posts = []

            for row in rows:

                posts.append({
                    "id": row[0],
                    "title": row[1],
                    "author": row[2],
                    "published_date": row[3].isoformat(),
                    "summary": row[4],
                    "url": row[5],
                    "scraped_at": row[6].isoformat()
                })

            return posts

    finally:
        connection.close()


def get_post_by_id(post_id):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    author,
                    published_date,
                    summary,
                    url,
                    scraped_at
                FROM blog_posts
                WHERE id = %s
                """,
                (post_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "id": row[0],
                "title": row[1],
                "author": row[2],
                "published_date": row[3].isoformat(),
                "summary": row[4],
                "url": row[5],
                "scraped_at": row[6].isoformat()
            }

    finally:
        connection.close()
