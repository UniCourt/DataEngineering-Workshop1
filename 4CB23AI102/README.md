# Python Blog Scraper

This is a Python-based web scraper that extracts posts from the official Python Insider blog and stores them in a PostgreSQL database using Docker Compose.

## How to Run the Scraper

1. Make sure Docker and Docker Compose are installed on your system.
2. In this directory, bring up the database container if it is not already running:
   ```bash
   docker-compose up -d psql-db
   ```
3. Run the interactive scraper application:
   ```bash
   docker-compose run app
   ```
4. Follow the on-screen prompts:
   - You can choose to search by `year` or `tag`.
   - Enter either `year` or `tag` and press enter for the follow up question.
   - If you leave the first prompt blank, it will scrape the default homepage.
   - Enter the number of pages you want to scrape.

## How to View the Database

The scraped data is stored in a PostgreSQL database container. To view the data, you can connect directly to the interactive database shell:

1. Open your terminal in this directory.
2. Run the following command to access the `psql` interface:
   ```bash
   docker exec -it psql-db psql -U postgres
   ```
3. Inside the `postgres=#` prompt, you can run SQL queries directly.:
   ```sql
   SELECT * FROM python_blog_posts;;
   ```
4. Other useful commands:
   - `\x` : Enables extended view. Recommended for viewing the full body of the posts.
   - `\d python_blog_posts` : Show the table schema.
   - `SELECT COUNT(*) FROM python_blog_posts;` : Count how many posts have been inserted.
   - `\q` : Quit the database interface.
