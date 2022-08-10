# Data Engineering Workshop

One Day workshop on understanding Docker, Web Scrapping, Regular Expressions, PostgreSQL and Git.

## Prerequisite

### Any Linux machine/VM with following packages installed
- Python 3.6 or above
- docker
- [docker-compose](https://docs.docker.com/compose/install/)
- pip3
- git (any recent version)

### GitHub account
- Create an account on [GitHub](https://github.com/join) (if you don't already have one)
- Fork [this](https://github.com/UniCourt/DataEngineering-Workshop1) repository and then clone it to your machine
- You can refer [this](https://docs.github.com/en/get-started/quickstart/fork-a-repo) guide to understand how to fork and clone

### Docker
- To install docker go to your cloned repository and run the following command
- `sudo prerequisites/install_docker.sh`

### Workshop environment setup 
 - Check if Git, Docker, and Docker Compose are installed in on the system. Open the terminal and run the following command
   ```
   Command: $ git --version
   git version 2.25.1

   Command: $ docker --version
   Docker version 20.10.17, build 100c701

   Command: $ docker-compose --version
   docker-compose version 1.25.0, build 0a186604

   ```

## What will you learn by the end of this workshop?
- By the end of this workshop you will learn how to build docker image and it's usage.
- You will learn how to scrape a website using urllib/requests and Beautifulsoup.
- You will learn Regular Expressions and how to work with it.
- You will learn key features of PostgreSQL.
- You will learn how to dockerize your project.

## Schedule
| Time                    | Topics
| ----------------------- |-------
| 09:00 - 11:00           |  [`Introduction to Docker`](/docs/introduction_to_docker.md)
| 11:00 - 01:00           |  [`Introduction to Webscrapping.`](/docs/introduction_to_webscraping.md)
| 1:00 -  2:00            |  `Break`
| 02:00 - 03:00           |  [`Introduction to PostgreSQL`](/docs/introduction_to_postgresql.md)
| 03:30 - 04:00           |  [`Dockerizing a project`](/docs/webscraping_with_docker.md)
| 04:00 - 04:30            |  [`Introduction to Github`](/docs/introduction_to_git_commands.md)
| 04:30 - 05:00            |  `Q & A and Wrapping Up`