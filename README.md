# Data Engineering Workshop 1

One-day workshop on Docker, web scraping, regular expressions, PostgreSQL, and Git.

## Prerequisites

### Operating system and tools

Use [Ubuntu 20.04 LTS](https://releases.ubuntu.com/focal/ubuntu-20.04.5-desktop-amd64.iso) (or a similar Linux desktop) with:

- Python 3.9 or above
- Docker
- [Docker Compose](https://docs.docker.com/compose/install/)
- `pip3`
- Git (any recent version)

### GitHub account

1. Create an account on [GitHub](https://github.com/join) if you do not already have one.
2. Fork the [DataEngineering-Workshop1](https://github.com/UniCourt/DataEngineering-Workshop1) repository. See [how to fork a repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo).
3. Clone your fork using SSH:
   - Set up an SSH key using the [GitHub SSH documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) if needed.
   - Open your forked repository in the browser.
   - Click **Code**, choose **SSH**, and copy the URL.
   - Clone the repository (replace `YOUR-GIT-ID` with your GitHub username):

```bash
git clone git@github.com:<YOUR-GIT-ID>/DataEngineering-Workshop1.git
```

### Install Docker

From your cloned repository, run:

```bash
sudo prerequisites/install_docker.sh
```

### Confirm your environment

```bash
git --version
docker --version
docker-compose --version
```

Example versions (yours may be newer):

- `git version 2.25.1`
- `Docker version 20.10.17`
- `docker-compose version 1.25.0`

## Learning outcomes

By the end of this workshop, you will be able to:

- Build and use Docker images
- Scrape a website using `requests` / `urllib` and BeautifulSoup
- Use regular expressions in scraping workflows
- Use key PostgreSQL features
- Dockerize a small project

## Schedule

| Time | Topics |
|------|--------|
| 09:00–11:00 | [Introduction to Docker](docs/introduction_to_docker.md) |
| 11:00–01:00 | [Introduction to Web Scraping](docs/introduction_to_webscraping.md) |
| 01:00–02:00 | Break |
| 02:00–03:00 | [Dockerizing a project](docs/working_with_docker_container.md) |
| 03:00–04:00 | [Introduction to PostgreSQL](docs/introduction_to_postgresql.md) |
| 04:00–04:30 | [Introduction to GitHub](docs/introduction_to_git_commands.md) |
| 04:30–04:45 | Q & A |
| 04:45–05:00 | [Wrapping Up](docs/workshop1_home_work.md) |
