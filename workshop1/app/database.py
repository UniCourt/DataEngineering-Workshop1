"""
database.py
------------
Handles the PostgreSQL connection and defines the table (model)
where scraped blog data will be stored.

We use SQLAlchemy because it lets us:
 - define the table structure as a Python class (a "model")
 - avoid writing raw SQL for basic inserts
 - easily swap databases later if needed
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# ---------------------------------------------------------------------------
# 1. Read DB connection details from environment variables.
#    Using env vars (instead of hardcoding) means the SAME code works both:
#      - when you run it locally, and
#      - when it runs inside Docker (where the DB host is a container name)
# ---------------------------------------------------------------------------
DB_USER = os.getenv("POSTGRES_USER", "bloguser")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "blogpass")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")   # will be "db" inside docker-compose
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "blogsdb")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ---------------------------------------------------------------------------
# 2. Create the SQLAlchemy engine + session factory
# ---------------------------------------------------------------------------
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


# ---------------------------------------------------------------------------
# 3. Define the table structure (this becomes a real SQL table)
# ---------------------------------------------------------------------------
class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), unique=True, nullable=False)  # avoid duplicate scrapes
    author = Column(String(255), nullable=True)
    published_date = Column(String(100), nullable=True)
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Create all tables if they don't already exist."""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Return a new DB session (like opening a connection to work with)."""
    return SessionLocal()
