### Webscrapping with docker.
   - Create a new docker file.
     
           FROM python:3.10.2-alpine3.15
           # Create directories  
           RUN mkdir -p /root/workspace/src
           COPY ./web_scraping_sample.py  /root/workspace/src
           # Switch to project directory
           WORKDIR /root/workspace/src
        
   - Create a docker-compose file.
     
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
   - Get the containers up.
     
            docker-compose up -d
     
   - Login to the container.
     
         docker exec -it python_service sh
   - Run the script for web scrapping inside the container.
      
         python web_scraping_sample.py