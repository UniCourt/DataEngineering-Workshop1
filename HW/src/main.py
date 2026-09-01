"""
main.py — Entry point for Workshop 1 scraper.

Flow:
  1. Connect to Postgres (with retry loop for Docker startup).
  2. Ensure schema exists (CREATE TABLE IF NOT EXISTS).
  3. Scrape sandbox pages index  → save to sandbox_pages.
  4. Scrape hockey teams (all pages) → save to hockey_teams.
  5. Log each run to scrape_runs for auditing.
"""

import logging
import os
import sys
from datetime import datetime

# ── Logging config ─────────────────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("/app/logs/scraper.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("main")

# ── Project imports ─────────────────────────────────────────────────────────
from database import (
    get_connection,
    init_schema,
    log_run,
    save_hockey_teams,
    save_sandbox_pages,
)
from scraper import HockeyTeamsScraper, SandboxPagesScraper


def run_sandbox_pages(conn) -> None:
    started = datetime.utcnow()
    try:
        pages  = SandboxPagesScraper().scrape()
        saved  = save_sandbox_pages(conn, pages)
        log_run(conn, "sandbox_pages", saved, "success", "", started, datetime.utcnow())
        logger.info("✔  sandbox_pages done — %d rows saved.", saved)
    except Exception as exc:
        log_run(conn, "sandbox_pages", 0, "error", str(exc), started, datetime.utcnow())
        logger.error("✖  sandbox_pages failed: %s", exc, exc_info=True)


def run_hockey_teams(conn) -> None:
    started = datetime.utcnow()
    try:
        teams  = HockeyTeamsScraper().scrape()
        saved  = save_hockey_teams(conn, teams)
        log_run(conn, "hockey_teams", saved, "success", "", started, datetime.utcnow())
        logger.info("✔  hockey_teams done — %d rows saved.", saved)
    except Exception as exc:
        log_run(conn, "hockey_teams", 0, "error", str(exc), started, datetime.utcnow())
        logger.error("✖  hockey_teams failed: %s", exc, exc_info=True)


def main() -> None:
    logger.info("=" * 60)
    logger.info("Workshop 1 Scraper — starting up")
    logger.info("=" * 60)

    with get_connection() as conn:
        # Ensure tables exist
        init_schema(conn)

        # Run both scrapers
        run_sandbox_pages(conn)
        run_hockey_teams(conn)

    logger.info("All done. Check your PostgreSQL DB for results.")


if __name__ == "__main__":
    main()
