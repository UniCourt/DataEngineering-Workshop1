CREATE TABLE IF NOT EXISTS python_blog_posts (
    id VARCHAR PRIMARY KEY,
    title VARCHAR,
    date VARCHAR,
    author VARCHAR,
    body TEXT,
    url VARCHAR,
    tags VARCHAR
);
