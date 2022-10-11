# Introduction to Docker

## Video : Introduction to Docker and Containers 


Docker is a container management service. The keywords of Docker are develop, ship and run anywhere. The whole idea of Docker is for developers to easily develop applications, ship them into containers which can then be deployed anywhere.

[![Video : Introduction to Docker and Containers](https://i3.ytimg.com/vi/JSLpG_spOBM/hqdefault.jpg)](https://www.youtube.com/watch?v=JSLpG_spOBM&ab_channel=RyanSchachte)

<br />

## Features of Docker

- Docker has the ability to reduce the size of development by providing a smaller footprint of the operating system via containers.

- With containers, it becomes easier for teams across different units, such as development, QA and Operations to work seamlessly across applications.

- You can deploy Docker containers anywhere, on any physical and virtual machines and even on the cloud.

- Since Docker containers are pretty lightweight, they are very easily scalable.

<br />

## Docker post-installation setup
Do the optional procedure configuration to work better with Docker.

### Run Docker as non-root user
To create the docker group and add your user:
1. Create the docker group.
```
sudo groupadd docker
```
2. Add your user to the docker group.
```
sudo usermod -aG docker $USER
```

3. Activate the changes to groups:
```
newgrp docker 
```
4. Verify that you can run docker commands without sudo.
```
docker images
```

<br />

## Docker Commands
Docker is a containerization system which packages and runs the application with its dependencies inside a container. There are several docker commands you must know when working with Docker.
### 1. Docker version
To find the installed docker version
Command:
```
docker  --version
```
##### **_Docker version 20.10.12, build e91ed57_**


<br>

### 2. Downloading image
To work with any ocker image we need to download the docker image first.<br /> 
Command:
```
docker pull <IMAGE>
```
Example of pulling alpine:latest image
```
docker pull alpine:latest
```
 _Note: You may find 1000s of docker images in [Docker Hub](https://hub.docker.com/)_ 

<br>

### 3. List all the docker images
To list all the images that is locallt available in the host machine, simply run the below command. This will list all the docker images in the local system.
<br />
Command:
```
docker images
```
```
Example:
REPOSITORY  TAG  IMAGE ID       CREATED      SIZE
alpine     latest  c059bfaa849c 6 weeks ago  5.59MB
```
<br>

### 4. Run docker image
The docker run command first creates a writeable container layer over the specified image, and then starts it using the specified command.
<br>
Command:
```
docker run [options] <IMAGE>
```
> Explore here: [https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)


Example of running alpine:latest image, the options -t allows us to access the terminal and -i gets stdin stream added. Basicaly using -ti adds the terminal driver.
```
docker run -t -i alpine:latest
```
OR
```
docker run -ti alpine:latest
```
_Note: You can use Ctrl+D to come out from the docker image._

<br />

## Create docker image for python:3.10.2-alpine3.15
   
Create a new file called _**Dockerfile**_ and then paste the below content
```
FROM python:3.10.2-alpine3.15
# Create directories  
RUN mkdir -p /root/workspace/src
# Switch to project directory
WORKDIR /root/workspace/src
```
Goto the directory where you created **Dockerfile**
```
docker build ./ -t simple_python
```
You may check the image you created using `docker images` command

Run the _**simple_python**_ image you created 
```
docker run -ti simple_python
```
