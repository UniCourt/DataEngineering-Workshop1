import requests
from bs4 import BeautifulSoup 
import psycopg2 


#make a request to the website
url='https://blog.python.org/'
response=requests.get(url)

#parse the html content using BeautifulSoup
soup=BeautifulSoup(response.content,'html.parser')

#find all article titles and links
titles=soup.find_all('h3',class_='blog-title')
dates=soup.find_all('h2',class_='date-header')
	
#connect to the PostgreSQL database
conn=psycopg2.connect(database="mydatabase",user="postgres",password="123456",host="localhost",port="5432")


#create a cursor object to execute SQL statements
cur=conn.cursor()

#create a table to store the blog data
cur.execute('CREATE TABLE IF NOT EXISTS blog (id SERIAL PRIMARY KEY,title TEXT, date DATE)')

#insert the blog post titles and links into the database
for i in range(len(titles)):
	title=titles[i].get_text()
	date=dates[i].get_text()
	cur.execute('INSERT INTO blog (title,date) VALUES (%s,%s)',(title,date))

#commit the changes and close the connection
conn.commit()
cur.close()
conn.close()




