# unicourtworkshop1

Scraped a pythonblog and stored the content in the postgresql in a database called pyscraper having a table pyscraper_table with the following attributes(id,date,title,author,content) .


# docker commands

docker-compose up --build

docker exec -it dataengineering-workshop1-db-1 psql -U postgres   #to activate the postgresql container in a interactive mode

# postgresql command 

\c pyscraper    #to connect to database
select * from pyscraper_table ;    #to view the table







