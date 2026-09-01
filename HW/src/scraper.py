"""
scraper.py — All scraping logic for scrapethissite.com.

Two scrapers:
  1. SandboxPagesScraper  → /pages/        (blog-like index of sandbox pages)
  2. HockeyTeamsScraper   → /pages/forms/  (paginated table of NHL team stats)

Both use a shared requests.Session with headers that mimic a real browser,
plus exponential-backoff retries for transient failures.
"""

import logging
import time
from typing import List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from models import HockeyTeam, SandboxPage

logger = logging.getLogger(__name__)

BASE_URL = "https://www.scrapethissite.com"

# ── Shared session ───────────────────────────────────────────────────────────

def _make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Connection": "keep-alive",
        }
    )
    return session


def _get_with_retry(session: requests.Session, url: str,
                    params: dict = None, retries: int = 3) -> requests.Response:
    """
    GET a URL with exponential backoff on 5xx or connection errors.
    Raises requests.HTTPError if all retries fail.
    """
    for attempt in range(1, retries + 1):
        try:
            resp = session.get(url, params=params, timeout=15)
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            wait = 2 ** attempt
            logger.warning("Request failed (attempt %d/%d) — %s. Retrying in %ds…",
                           attempt, retries, exc, wait)
            if attempt == retries:
                raise
            time.sleep(wait)


# ── Helper ───────────────────────────────────────────────────────────────────

def _to_int(text: str) -> Optional[int]:
    text = text.strip()
    try:
        return int(text) if text else None
    except ValueError:
        return None


def _to_float(text: str) -> Optional[float]:
    text = text.strip()
    try:
        return float(text) if text else None
    except ValueError:
        return None


# ── Scraper 1: Sandbox Pages Index ───────────────────────────────────────────

class SandboxPagesScraper:
    """
    Scrapes the listing at /pages/ and returns each sandbox page
    as a SandboxPage dataclass (title, URL, description).

    Structure of each entry on the page:

        <div class="page">
          <h3 class="page-title"><a href="/pages/simple/">Countries…</a></h3>
          <p class="lead">A single page that lists…</p>
        </div>
    """

    TARGET = "/pages/"

    def __init__(self):
        self.session = _make_session()

    def scrape(self) -> List[SandboxPage]:
        url = urljoin(BASE_URL, self.TARGET)
        logger.info("Scraping sandbox pages index: %s", url)

        resp = _get_with_retry(self.session, url)
        soup = BeautifulSoup(resp.text, "lxml")

        pages: List[SandboxPage] = []

        for div in soup.select("div.page"):
            # Title and relative URL live in the <a> inside the heading
            a_tag = div.select_one("h3.page-title a, .page-title a, h3 a")
            desc_tag = div.select_one("p.lead, p.description")

            if not a_tag:
                continue

            title = a_tag.get_text(strip=True)
            href  = a_tag.get("href", "")
            full_url = urljoin(BASE_URL, href)
            description = desc_tag.get_text(strip=True) if desc_tag else ""

            pages.append(SandboxPage(title=title, url=full_url, description=description))
            logger.debug("Found page: %s", title)

        logger.info("Scraped %d sandbox pages.", len(pages))
        return pages


# ── Scraper 2: Hockey Teams (paginated) ──────────────────────────────────────

class HockeyTeamsScraper:
    """
    Scrapes the multi-page NHL team stats table at /pages/forms/.

    Each page is fetched via:
        GET /pages/forms/?page_num=<N>

    Pagination is detected by counting <a> links in .pagination and
    iterating until no new teams are returned.

    Row structure (one <tr class="team"> per team):

        <td class="name">Boston Bruins</td>
        <td class="year">1990</td>
        <td class="wins">44</td>
        <td class="losses">24</td>
        <td class="ot-losses"></td>
        <td class="pct">0.55</td>
        <td class="gf">299</td>
        <td class="ga">264</td>
        <td class="diff">35</td>
    """

    TARGET = "/pages/forms/"
    DELAY_BETWEEN_PAGES = 1.0  # seconds — be polite to the server

    def __init__(self):
        self.session = _make_session()

    def _get_total_pages(self, soup: BeautifulSoup) -> int:
        """Parse the pagination widget to find the last page number."""
        page_links = soup.select("ul.pagination li a")
        numbers = []
        for link in page_links:
            text = link.get_text(strip=True)
            try:
                numbers.append(int(text))
            except ValueError:
                pass
        return max(numbers) if numbers else 1

    def _parse_teams(self, soup: BeautifulSoup) -> List[HockeyTeam]:
        teams: List[HockeyTeam] = []
        for row in soup.select("tr.team"):
            cells = row.find_all("td")
            if len(cells) < 9:
                continue

            teams.append(
                HockeyTeam(
                    team_name=    cells[0].get_text(strip=True),
                    year=         _to_int(cells[1].get_text()) or 0,
                    wins=         _to_int(cells[2].get_text()),
                    losses=       _to_int(cells[3].get_text()),
                    ot_losses=    _to_int(cells[4].get_text()),
                    win_pct=      _to_float(cells[5].get_text()),
                    goals_for=    _to_int(cells[6].get_text()),
                    goals_against=_to_int(cells[7].get_text()),
                    plus_minus=   _to_int(cells[8].get_text()),
                )
            )
        return teams

    def scrape(self) -> List[HockeyTeam]:
        url = urljoin(BASE_URL, self.TARGET)
        all_teams: List[HockeyTeam] = []

        # ── Page 1: also tells us how many pages exist ──
        logger.info("Fetching page 1 of hockey teams…")
        resp = _get_with_retry(self.session, url, params={"page_num": 1})
        soup = BeautifulSoup(resp.text, "lxml")

        total_pages = self._get_total_pages(soup)
        logger.info("Detected %d total pages.", total_pages)

        all_teams.extend(self._parse_teams(soup))

        # ── Remaining pages ──
        for page in range(2, total_pages + 1):
            logger.info("Fetching page %d / %d…", page, total_pages)
            time.sleep(self.DELAY_BETWEEN_PAGES)
            resp = _get_with_retry(self.session, url, params={"page_num": page})
            soup = BeautifulSoup(resp.text, "lxml")
            teams_on_page = self._parse_teams(soup)
            if not teams_on_page:
                logger.info("No more teams on page %d — stopping.", page)
                break
            all_teams.extend(teams_on_page)

        logger.info("Scraped %d hockey team records in total.", len(all_teams))
        return all_teams
