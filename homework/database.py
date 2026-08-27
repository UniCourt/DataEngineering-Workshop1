import os
import time

import psycopg2
from psycopg2.extras import execute_values


def get_connection():
    """
    Create a PostgreSQL connection using environment variables.
    """

    host = os.getenv(
        "DB_HOST",
        "localhost",
    )

    port = os.getenv(
        "DB_PORT",
        "5432",
    )

    database = os.getenv(
        "POSTGRES_DB",
        "python_blogs",
    )

    user = os.getenv(
        "POSTGRES_USER",
        "postgres",
    )

    password = os.getenv(
        "POSTGRES_PASSWORD",
        "postgres",
    )

    return psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
    )


def wait_for_database(
    retries=10,
    delay=2,
):
    """
    Wait until PostgreSQL is ready.
    """

    for attempt in range(
        1,
        retries + 1,
    ):
        try:
            connection = get_connection()

            connection.close()

            print("PostgreSQL is ready.")

            return

        except psycopg2.OperationalError:
            print(
                f"Waiting for PostgreSQL... "
                f"attempt {attempt}/{retries}"
            )

            time.sleep(delay)

    raise RuntimeError(
        "Could not connect to PostgreSQL."
    )


def save_blogs(blogs):
    """
    Insert scraped blog posts into PostgreSQL.

    Existing URLs are ignored so that
    duplicate blog posts are not created.
    """

    if not blogs:
        print("No blogs to insert.")

        return

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            query = """
                INSERT INTO blogs (
                    title,
                    author,
                    published_date,
                    description,
                    url
                )
                VALUES %s
                ON CONFLICT (url) DO NOTHING;
            """

            values = [
                (
                    blog["title"],
                    blog["author"],
                    blog["published_date"],
                    blog["description"],
                    blog["url"],
                )
                for blog in blogs
            ]

            execute_values(
                cursor,
                query,
                values,
            )

            inserted_count = cursor.rowcount

        connection.commit()

        skipped_count = (
            len(blogs) - inserted_count
        )

        print(
            f"New blog records inserted: "
            f"{inserted_count}"
        )

        print(
            f"Existing/duplicate records skipped: "
            f"{skipped_count}"
        )

    except Exception:
        connection.rollback()

        raise

    finally:
        connection.close()