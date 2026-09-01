"""
database.py — PostgreSQL connection, table init, and insert helpers.

Uses psycopg2 directly (no ORM) so the SQL is transparent and easy
to read during a workshop session.
"""

import logging
import os
import time
from contextlib import contextmanager
from datetime import datetime
from typing import List

import psycopg2
import psycopg2.extras
from psycopg2 import OperationalError

from models import HockeyTeam, SandboxPage

logger = logging.getLogger(__name__)


# ── Connection ─────────────────────────────────────────────────────────────

def _build_dsn() -> str:
    return (
        f"host={os.getenv('DB_HOST', 'localhost')} "
        f"port={os.getenv('DB_PORT', '5432')} "
        f"dbname={os.getenv('DB_NAME', 'scraper_db')} "
        f"user={os.getenv('DB_USER', 'scraper_user')} "
        f"password={os.getenv('DB_PASSWORD', 'scraper_pass')}"
    )


def wait_for_db(retries: int = 10, delay: int = 3) -> psycopg2.extensions.connection:
    """
    Retry connecting to Postgres until it is ready.
    Docker starts the DB container before the scraper, but Postgres
    itself may still be initialising when the scraper tries to connect.
    """
    for attempt in range(1, retries + 1):
        try:
            conn = psycopg2.connect(_build_dsn())
            logger.info("Connected to PostgreSQL on attempt %d.", attempt)
            return conn
        except OperationalError as exc:
            logger.warning("DB not ready (attempt %d/%d): %s", attempt, retries, exc)
            if attempt == retries:
                raise
            time.sleep(delay)


@contextmanager
def get_connection():
    """Context manager — always commits or rolls back, then closes."""
    conn = wait_for_db()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ── Schema bootstrap ────────────────────────────────────────────────────────

def init_schema(conn: psycopg2.extensions.connection) -> None:
    """
    Run the SQL file that creates tables if they do not already exist.
    Called once at startup so the schema is always in sync.
    """
    sql_path = os.path.join(os.path.dirname(__file__), "..", "sql", "init.sql")
    with open(sql_path) as fh:
        ddl = fh.read()
    with conn.cursor() as cur:
        cur.execute(ddl)
    conn.commit()
    logger.info("Schema initialised.")


# ── Inserts ─────────────────────────────────────────────────────────────────

def save_sandbox_pages(conn, pages: List[SandboxPage]) -> int:
    """
    Upsert sandbox pages — skip duplicates (same URL) rather than crash.
    Returns the number of rows actually inserted.
    """
    records = [
        {
            "title": p.title,
            "url": p.url,
            "description": p.description,
            "scraped_at": p.scraped_at,
        }
        for p in pages
    ]
    inserted = 0
    with conn.cursor() as cur:
        for rec in records:
            cur.execute(
                """
                INSERT INTO sandbox_pages (title, url, description, scraped_at)
                VALUES (%(title)s, %(url)s, %(description)s, %(scraped_at)s)
                ON CONFLICT (url) DO NOTHING
                """,
                rec,
            )
            inserted += cur.rowcount
    conn.commit()
    logger.info("sandbox_pages: %d new rows inserted (out of %d scraped).", inserted, len(pages))
    return inserted


def save_hockey_teams(conn, teams: List[HockeyTeam]) -> int:
    """
    Upsert hockey team rows — skip duplicates (same team_name + year).
    Returns the number of rows actually inserted.
    """
    inserted = 0
    with conn.cursor() as cur:
        for t in teams:
            cur.execute(
                """
                INSERT INTO hockey_teams
                    (team_name, year, wins, losses, ot_losses,
                     win_pct, goals_for, goals_against, plus_minus, scraped_at)
                VALUES
                    (%(team_name)s, %(year)s, %(wins)s, %(losses)s, %(ot_losses)s,
                     %(win_pct)s, %(goals_for)s, %(goals_against)s, %(plus_minus)s, %(scraped_at)s)
                ON CONFLICT (team_name, year) DO NOTHING
                """,
                {
                    "team_name":     t.team_name,
                    "year":          t.year,
                    "wins":          t.wins,
                    "losses":        t.losses,
                    "ot_losses":     t.ot_losses,
                    "win_pct":       t.win_pct,
                    "goals_for":     t.goals_for,
                    "goals_against": t.goals_against,
                    "plus_minus":    t.plus_minus,
                    "scraped_at":    t.scraped_at,
                },
            )
            inserted += cur.rowcount
    conn.commit()
    logger.info("hockey_teams: %d new rows inserted (out of %d scraped).", inserted, len(teams))
    return inserted


def log_run(conn, target: str, rows_saved: int, status: str = "success",
            message: str = "", started_at: datetime = None, finished_at: datetime = None) -> None:
    """Record a scrape run in the scrape_runs audit table."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO scrape_runs (target, rows_saved, status, message, started_at, finished_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (target, rows_saved, status, message, started_at or datetime.utcnow(), finished_at),
        )
    conn.commit()
