# Data Engineering Workshop

One Day workshop on understanding Docker, Web Scrapping, Regular Expressions, PostgreSQL and Git.

## Prerequisites

### Use [Ubuntu 20.04 LTS](https://releases.ubuntu.com/focal/ubuntu-20.04.5-desktop-amd64.iso) with following packages installed
- Python 3.9 or above
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
     
 ### Homework
  - Run docker-compose.yml with posgresql commands to start server 
    ```
    docker-compose up -d 
    ```
    ```
    docker exec -it psql-db bash
    ```
    ```
    psql -U postgres
    ```
     - create a database to store the scraped content
     
  - Run Dockerfile using commands
    ```
    docker build --no-cache --network=host ./ -t simple_python 
    ```      
    ```
    docker run --network=host simple_python
    ```
    
  - The scraped content will be stored in a table format 
    - Date | Title | Content/BodyText | Author
  
  
