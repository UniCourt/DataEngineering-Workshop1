"""
models.py — Plain dataclasses that represent scraped records.
No ORM dependency; maps 1-to-1 with the DB tables in init.sql.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class SandboxPage:
    """
    One entry from the scrapethissite.com /pages/ index.
    Treated as a 'blog post' entry for this workshop.
    """
    title: str
    url: str
    description: str
    scraped_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class HockeyTeam:
    """
    One row from the paginated Hockey Teams table at /pages/forms/.
    """
    team_name: str
    year: int
    wins: Optional[int] = None
    losses: Optional[int] = None
    ot_losses: Optional[int] = None
    win_pct: Optional[float] = None
    goals_for: Optional[int] = None
    goals_against: Optional[int] = None
    plus_minus: Optional[int] = None
    scraped_at: datetime = field(default_factory=datetime.utcnow)
