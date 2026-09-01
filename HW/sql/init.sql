-- =========================================================
-- Workshop 1 — Schema
-- =========================================================

-- Sandbox pages scraped from /pages/ index (treated as blog entries)
CREATE TABLE IF NOT EXISTS sandbox_pages (
    id           SERIAL PRIMARY KEY,
    title        VARCHAR(500) NOT NULL,
    url          TEXT         NOT NULL UNIQUE,
    description  TEXT,
    scraped_at   TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- Hockey team records scraped from /pages/forms/ (paginated)
CREATE TABLE IF NOT EXISTS hockey_teams (
    id            SERIAL PRIMARY KEY,
    team_name     VARCHAR(255) NOT NULL,
    year          INTEGER      NOT NULL,
    wins          INTEGER,
    losses        INTEGER,
    ot_losses     INTEGER,
    win_pct       NUMERIC(6,4),
    goals_for     INTEGER,
    goals_against INTEGER,
    plus_minus    INTEGER,
    scraped_at    TIMESTAMP    NOT NULL DEFAULT NOW(),
    UNIQUE (team_name, year)
);

-- Simple log table so you can track each scrape run
CREATE TABLE IF NOT EXISTS scrape_runs (
    id          SERIAL PRIMARY KEY,
    target      VARCHAR(255) NOT NULL,
    rows_saved  INTEGER      NOT NULL DEFAULT 0,
    status      VARCHAR(50)  NOT NULL DEFAULT 'success',
    message     TEXT,
    started_at  TIMESTAMP    NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMP
);
