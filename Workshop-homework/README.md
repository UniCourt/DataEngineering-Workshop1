# Python Blog Scraper with Docker and PostgreSQL

A containerized Python web scraper that extracts blog post titles and URLs from the [Python Insider Blog](https://blog.python.org/) and stores the collected data in a PostgreSQL database.

The project uses Docker Compose to run the scraper and PostgreSQL as separate containers that communicate through a Docker network.

## Overview

This project demonstrates a simple data pipeline where web data is collected, processed, and stored in a relational database.

The application performs the following steps:

1. Starts a PostgreSQL database using Docker.
2. Waits until PostgreSQL is ready to accept connections.
3. Starts the Python scraper.
4. Fetches the Python Insider Blog using `Requests`.
5. Parses the webpage using `BeautifulSoup`.
6. Extracts blog titles and URLs.
7. Connects to PostgreSQL using `Psycopg`.
8. Creates the database table if it does not already exist.
9. Stores the scraped blog posts in PostgreSQL.
10. Prevents duplicate blog URLs from being inserted.

## Technologies Used

- **Python 3.10**
- **Requests** – HTTP requests
- **BeautifulSoup4** – HTML parsing
- **Psycopg** – PostgreSQL connectivity
- **PostgreSQL 14** – Database
- **Docker** – Containerization
- **Docker Compose** – Multi-container application management
- **Alpine Linux** – Lightweight Docker base image

## Project Structure

```text
workshop_homework1/
│
├── Dockerfile
├── docker-compose.yaml
├── entry.sh
├── requirements.txt
├── scrapper.py
├── scraper.py
├── .gitignore
└── README.md
```

## File Descriptions

### Dockerfile

Defines the Docker image used to run the Python scraper.

It:

- Uses Python 3.10 Alpine as the base image.
- Sets `/app` as the working directory.
- Installs the required Python dependencies.
- Copies the project files into the container.
- Gives execution permission to `entry.sh`.
- Starts the application through `entry.sh`.

### docker-compose.yaml

Defines and manages the two services used by the project:

- `blog_scraper`
- `homework-psql-db`

Docker Compose also creates a shared network that allows the scraper container to communicate with the PostgreSQL container.

### scrapper.py

Contains the main scraping logic.

The script:

- Sends a request to the Python Insider Blog.
- Checks the HTTP response status.
- Parses the HTML content.
- Extracts blog titles and URLs.
- Connects to PostgreSQL.
- Creates the `blog_posts` table if required.
- Inserts the scraped data.
- Prevents duplicate URLs.
- Displays the number of stored blog posts.

### entry.sh

Controls the startup process of the scraper container.

It waits for PostgreSQL to become available before running the Python scraper.

This is important because Docker starts containers independently, and the scraper may start before PostgreSQL has finished initializing.

### requirements.txt

Contains the Python packages required by the scraper.

```text
requests
beautifulsoup4
psycopg[binary]
```

### .gitignore

Contains files and directories that should not be tracked by Git.

## How the Project Works

The application follows this flow:

```text
                Python Insider Blog
                         |
                         v
                  HTTP Request
                         |
                         v
                 Python Scraper
                         |
                         v
                  BeautifulSoup
                         |
                         v
              Extract Title + URL
                         |
                         v
                PostgreSQL Database
                         |
                         v
                   blog_posts
```

The scraper and database run in separate Docker containers:

```text
+----------------------+       +-------------------------+
|    blog_scraper      |       |    homework-psql-db     |
|                      |       |                         |
|  Python              |       |  PostgreSQL 14          |
|  Requests            | ----> |  Database: demo         |
|  BeautifulSoup       |       |  Port: 5432             |
|  Psycopg             |       |                         |
+----------------------+       +-------------------------+
             \                       /
              \_____________________/
                 Docker Network
```

## Web Scraping

The scraper fetches the Python Insider Blog:

```text
https://blog.python.org/
```

It sends an HTTP request using the Requests library.

The response is then passed to BeautifulSoup for HTML parsing.

The scraper searches for blog headings and extracts:

- Blog title
- Blog URL

Example:

```text
Title: Python 3.15.0 beta 3 is here!
URL: https://blog.python.org/2026/06/python-3150-beta-3/
```

## PostgreSQL Database

The scraped data is stored in a PostgreSQL database named:

```text
demo
```

The application connects to PostgreSQL using the Docker service name:

```text
psql-db
```

The internal PostgreSQL port is:

```text
5432
```

The scraper creates the following table:

```sql
CREATE TABLE IF NOT EXISTS blog_posts(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL
);
```

The table contains three columns:

| Column | Description |
|---|---|
| `id` | Unique identifier for each blog |
| `title` | Title of the blog post |
| `url` | URL of the blog post |

## Duplicate Prevention

The `url` column is defined as `UNIQUE`.

The scraper also uses:

```sql
ON CONFLICT (url) DO NOTHING
```

This prevents the same blog post from being inserted multiple times if the scraper is executed again.

## Docker Architecture

The project uses two containers.

### Blog Scraper Container

The `blog_scraper` container contains:

- Python
- Requests
- BeautifulSoup
- Psycopg
- Scraping logic

Its responsibility is to collect data from the Python Insider Blog and store it in PostgreSQL.

### PostgreSQL Container

The `homework-psql-db` container runs PostgreSQL 14.

Its responsibility is to store the scraped blog data.

### Communication Between Containers

The containers communicate through the Docker Compose network.

The scraper does not use `localhost` to connect to PostgreSQL.

Instead, it uses:

```text
psql-db:5432
```

Here, `psql-db` is the PostgreSQL service name defined in Docker Compose.

## Prerequisites

Before running the project, make sure you have:

- Docker installed
- Docker Compose available through Docker
- Git installed (optional, for cloning the repository)

You can verify Docker with:

```bash
docker --version
```

and Docker Compose with:

```bash
docker compose version
```

## Getting Started

Clone the repository:

```bash
git clone git@github.com:praveeksha04/Workshop-homework.git
```

Move into the project directory:

```bash
cd workshop_homework1
```

## Build the Docker Image

Build the project using:

```bash
docker compose build
```

This reads the `Dockerfile`, installs the Python dependencies, and creates the Docker image.

## Run the Application

Start the application using:

```bash
docker compose up
```

Docker Compose starts both services:

```text
blog_scraper
homework-psql-db
```

The scraper waits for PostgreSQL to become ready and then starts scraping the website.

## Run in Background

To run the application without keeping the terminal attached to the container logs:

```bash
docker compose up -d
```

You can check the running containers with:

```bash
docker compose ps
```

## View Application Logs

To view the scraper logs:

```bash
docker compose logs blog_scraper
```

To view PostgreSQL logs:

```bash
docker compose logs homework-psql-db
```

To follow all logs:

```bash
docker compose logs -f
```

## Access the PostgreSQL Database

Once the PostgreSQL container is running, open the PostgreSQL shell using:

```bash
docker exec -it homework-psql-db psql -U postgres -d demo
```

## View Database Tables

Inside the PostgreSQL shell, run:

```sql
\dt
```

You should see the `blog_posts` table.

## View Scraped Blog Posts

Run:

```sql
SELECT * FROM blog_posts;
```

This displays the stored blog titles and URLs.

## Count Stored Blog Posts

Run:

```sql
SELECT COUNT(*) FROM blog_posts;
```

Example:

```text
 count
-------
    50
```

The exact number may change depending on the content available on the Python Insider Blog when the scraper runs.

## Exit PostgreSQL

To exit the PostgreSQL shell:

```text
\q
```

If PostgreSQL displays query results inside a pager showing:

```text
(END)
```

press:

```text
q
```

first to return to the PostgreSQL prompt.

Then use:

```text
\q
```

to exit PostgreSQL.

## Stop the Application

If `docker compose up` is running in the foreground, press:

```text
Ctrl + C
```

You can also stop the application using:

```bash
docker compose down
```

This stops and removes the containers and the Docker network created by Compose.

## Rebuild After Making Changes

If you modify the Python code or Docker configuration, rebuild the image using:

```bash
docker compose up --build
```

This rebuilds the image before starting the containers.

## Database Credentials

The PostgreSQL connection uses the database configuration defined by the project.

The application connects using:

```text
Host: psql-db
Port: 5432
Database: demo
User: postgres
```

For development purposes, the database credentials are configured in the project.

For production applications, credentials should not be hardcoded in source code. Environment variables or Docker secrets should be used instead.

## Example Output

A successful run produces output similar to:

```text
Starting Python Blog Scraper...
Waiting for PostgreSQL...
PostgreSQL is ready!
Running scraper...
Fetching Python Blog...
Status: 200

Total blogs found: 50

Connecting to PostgreSQL...

Blogs saved to PostgreSQL
Total blogs in PostgreSQL: 50

Scraper completed successfully.
```

The exact number of blogs may vary depending on the website content at the time of execution.

## Error Handling

The scraper checks the HTTP response status before processing the webpage.

If the website cannot be fetched successfully, the scraper reports the failure instead of continuing with invalid content.

The startup script also waits for PostgreSQL before running the scraper, reducing database connection failures caused by PostgreSQL still being initialized.

## Key Concepts Demonstrated

This project demonstrates practical usage of:

- Web scraping
- HTTP requests
- HTML parsing
- Python scripting
- PostgreSQL
- SQL
- Database constraints
- Docker images
- Docker containers
- Docker Compose
- Container networking
- Service-to-service communication
- Shell scripting
- Database persistence
- Application startup dependencies

## Learning Outcomes

By building this project, the following concepts can be understood:

- How a Python program can collect data from a website.
- How HTML can be parsed using BeautifulSoup.
- How Python applications connect to PostgreSQL.
- How Docker isolates an application inside a container.
- How multiple containers communicate through Docker networking.
- How Docker Compose manages multiple services.
- Why an application may need to wait for a database before connecting.
- How scraped data can be stored and queried using SQL.
- How database constraints can prevent duplicate records.

## Future Improvements

Possible improvements include:

- Scraping additional information such as publication dates and descriptions.
- Adding pagination support.
- Scheduling automatic scraping.
- Adding better logging.
- Adding environment variables for configuration.
- Adding PostgreSQL health checks.
- Creating a REST API for the stored blog data.
- Building a frontend to display the scraped blogs.
- Adding automated tests.
- Deploying the application to a cloud platform.

## License

This project is created for learning and educational purposes.

## Acknowledgements

The project uses the Python Insider Blog as the source website for demonstrating web scraping.

Python Insider:

https://blog.python.org/

## Author

**Moolya Praveeksha Narayan**

B.E. Computer Science and Engineering

Canara Engineering College
