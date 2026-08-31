CREATE TABLE IF NOT EXISTS blog_posts (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    published_date TIMESTAMPTZ NOT NULL,
    summary TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    scraped_at TIMESTAMPTZ NOT NULL
);
