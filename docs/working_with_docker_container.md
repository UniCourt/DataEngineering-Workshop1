# Working with Docker container
<br />

```Introduction
A Docker container image is a lightweight, standalone, executable package of software that includes everything needed 
to run an application: code, runtime, system tools, system libraries and settings
```
> Explore [here](https://www.geeksforgeeks.org/python-urllib-module/)

<br />

### Docker Compose

```Introduction
Compose is a tool for defining and running multi-container Docker applications. 
With Compose, you use a YAML file to configure your application’s services. 
Then, with a single command, you create and start all the services from your configuration.
```
> Explore [here](https://docs.docker.com/compose/)

<br />

### Exercise

```
   - Create a new docker file.
     
           FROM python:3.10.2-alpine3.15
           # Create directories  
           RUN mkdir -p /root/workspace/src
           COPY ./web_scraping_sample.py  /root/workspace/src
           # Switch to project directory
           WORKDIR /root/workspace/src
```
<br />

```
Create a docker-compose file.
Filename: docker-compose.yml
     
version: "3"
services:
 pyhton_service:
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
<br />

```
Get the containers up.
     docker-compose up -d
```
<br />

```
Login to the container.
     docker exec -it python_service sh
```
<br />

```
Run the script for web scrapping inside the container.
     python web_scraping_sample.py
```