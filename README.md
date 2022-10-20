# Data Engineering Workshop

One Day workshop on understanding Docker, Web Scrapping, Regular Expressions, PostgreSQL and Git.

## Prerequisites

### Any Linux machine/VM with following packages installed
- Python 3.6 or above
- docker
- [docker-compose](https://docs.docker.com/compose/install/)
- pip3
- git (any recent version)

### GitHub account
- Create an account on [GitHub](https://github.com/join) (Only if you do not have an account)
- Fork [DataEngineering-Workshop1](https://github.com/UniCourt/DataEngineering-Workshop1) repository. Refer [this](https://docs.github.com/en/get-started/quickstart/fork-a-repo) guide to understand how to fork a repository
- Clone forked repo to your machine using SSH Key. 
  - Make sure you have set up SSH key as per the [documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to create a new SSH Key if you don't have a Key.
  - Open your forked repo link in your browser. 
  - Click on Code (Green color button).
  - Select SSH option and copy the link.
  - Clone the repo (replace YOUR-GIT-ID with your GitHub id)
    ```
       git clone git@github.com:<YOUR-GIT-ID>/DataEngineering-Workshop1.git
    ```

### Docker
- To install docker go to your cloned repository and run the following command
- `sudo prerequisites/install_docker.sh`

### Workshop environment setup 
 - Check if Git, Docker, and Docker Compose are installed in on the system. 
 - Open the terminal and run the following command to check the version of the prerequisites
   - Check Git version 
      ```
       git --version
      ```
     #####  **_git version 2.25.1_**
   -  Check Docker version
      ```
       docker --version
      ```
      ##### **_Docker version 20.10.17, build 100c701_**
   - Check Docker Compose version
      ```
       docker-compose --version
      ```
     ##### **_docker-compose version 1.25.0, build 0a186604_**

## What will you learn by the end of this workshop?
- By the end of this workshop you will learn how to build docker image and it's usage.
- You will learn how to scrape a website using urllib/requests and Beautifulsoup.
- You will learn Regular Expressions and how to work with it.
- You will learn key features of PostgreSQL.
- You will learn how to dockerize your project.

## Schedule
| Time          | Topics
|---------------|-------
| 09:00 - 11:00 |  [`Introduction to Docker`](/docs/introduction_to_docker.md)
| 11:00 - 01:00 |  [`Introduction to Webscrapping.`](/docs/introduction_to_webscraping.md)
| 01:00 - 02:00 |  `Break`
| 02:00 - 03:00 |  [`Dockerizing a project`](/docs/working_with_docker_container.md)
| 03:00 - 04:00 |  [`Introduction to PostgreSQL`](/docs/introduction_to_postgresql.md)
| 04:00 - 04:30 |  [`Introduction to Github`](/docs/introduction_to_git_commands.md)
| 04:30 - 04:45 |  `Q & A`
| 04:45 - 05:00 |  [`Wrapping Up`](/docs/workshop1_home_work.md)