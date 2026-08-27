CREATE TABLE IF NOT EXISTS blogs (
    id SERIAL PRIMARY KEY,

    title TEXT NOT NULL,

    author TEXT,

    published_date DATE,

    description TEXT,

    url TEXT UNIQUE NOT NULL,

    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);