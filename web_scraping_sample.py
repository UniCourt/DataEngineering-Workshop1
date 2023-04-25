import requests
from bs4 import BeautifulSoup
import psycopg2

url = 'https://blog.python.org/'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

titles = soup.find_all('h3', class_='post-title')
dates = soup.find_all('h2', class_='date-header')

conn = psycopg2.connect(database="mydatabase", user="postgres", password="123456", host="lostgres_service")#, #port="5432")


cur = conn.cursor()


cur.execute('CREATE TABLE IF NOT EXISTS blog (id SERIAL PRIMARY KEY, title TEXT, date DATE)')

for i in range(len(titles)):
    title = titles[i].get_text()
    date = dates[i].get_text()
    cur.execute('INSERT INTO blog (title, date) VALUES (%s, %s)', (title, date))


conn.commit()
cur.close()
conn.close()

