### Introduction to Docker.

    - Building the Docker image for Worker using python:3.10.2-alpine3.15
   
    * ***docker***
   
        Docker is a container management service. The keywords of Docker are   develop, ship and run anywhere. The whole idea of Docker is for developers to easily develop applications, ship them into containers which can then be deployed anywhere.
    * ***Images***
   
        Docker images are read-only templates with instructions to create a docker container. Docker image can be pulled from a Docker hub and used as it is, or you can add additional instructions to the base image and create a new and modified docker image. You can create your own docker images also using a dockerfile. Create a dockerfile with all the instructions to create a container and run it; it will create your custom docker image.
    * ***To create docker image for python:3.10.2-alpine3.15***
   
        1)Create a  dockerfile
		
                FROM python:3.10.2-alpine3.15
                # Create directories  
                RUN mkdir -p /root/workspace/src
                # Switch to project directory
                WORKDIR /root/workspace/src

        2)Goto the directory where you created Dockerfile
   
                docker build ./ -t Simple_python
