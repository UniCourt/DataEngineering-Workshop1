import requests
from bs4 import BeautifulSoup
import psycopg2

# Send a GET request to the website
url = 'https://blog.python.org/'
response = requests.get(url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the blog post titles and dates
titles = soup.find_all('h3', class_='post-title')
dates = soup.find_all('h2', class_='date-header')

# Create a connection to the PostgreSQL database
conn = psycopg2.connect(database="mydatabase", user="postgres", password="123456", host="lostgres_service")#, #port="5432")

# Create a cursor object to execute SQL statements
cur = conn.cursor()

# Create a table to store the blog data
cur.execute('CREATE TABLE IF NOT EXISTS blog (id SERIAL PRIMARY KEY, title TEXT, date DATE)')

# Insert the blog post titles and dates into the database
for i in range(len(titles)):
    title = titles[i].get_text()
    date = dates[i].get_text()
    cur.execute('INSERT INTO blog (title, date) VALUES (%s, %s)', (title, date))

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

