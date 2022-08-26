# Working with Docker container
<br />

```Introduction
A Docker container image is a lightweight, standalone, executable package of software that includes everything needed 
to run an application: code, runtime, system tools, system libraries and settings
```
> Explore here: [https://www.docker.com/resources/what-container/#:~:text=A%20Docker%20container%20image%20is,tools%2C%20system%20libraries%20and%20settings.](https://www.docker.com/resources/what-container/#:~:text=A%20Docker%20container%20image%20is,tools%2C%20system%20libraries%20and%20settings.)

<br />

### Docker Compose

```Introduction
Compose is a tool for defining and running multi-container Docker applications. 
With Compose, you use a YAML file to configure your application’s services. 
Then, with a single command, you create and start all the services from your configuration.
```
> Explore here: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)

<br />

### Exercise
 - Create a new docker file.
    ```
    FROM python:3.10.2-alpine3.15
    # Create directories  
    RUN mkdir -p /root/workspace/src
    COPY ./web_scraping_sample.py  /root/workspace/src
    # Switch to project directory
    WORKDIR /root/workspace/src
    # Install required packages
    RUN pip install --upgrade pip
    RUN pip install requests bs4 html5lib
    ```
 - Build docker image
    ```
    docker build --no-cache --network=host ./ -t workshop1 
    ```
 - Create a docker-compose file.
   - Filename: docker-compose.yml
    ```  
    version: "3"
    services:
     python_service:
       build:
         context: ./
         dockerfile: Dockerfile
       image: workshop1
       container_name: workshop_python_container
       stdin_open: true #  docker attach container_id
       tty: true
       ports:
        - "8000:8000"
       volumes:
        - .:/app
    ```

- Get the containers up.
    ``` 
     docker-compose up -d
    ```
- Login to the container.
    ```
     docker exec -it workshop_python_container sh
    ```
- Run the script for web scrapping inside the container.
    ```
     python web_scraping_sample.py
    ```