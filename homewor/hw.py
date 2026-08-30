import requests
from bs4 import BeautifulSoup
import re
import psycopg2


conn = psycopg2.connect(
     host="172.17.0.2",
      database="pybd",
    user="postgres",
    password="123456"
)

print("done\n")
cur = conn.cursor()

res = requests.get("https://www.python.org/")
soup = BeautifulSoup(res.content, 'html.parser')
    
titles=[]
prases=[]
   
for i in soup.find_all('h1'):
	string = i.getText()
	titles.append(string.strip())


		
for i in range(4):	   
	cur.execute(
	"INSERT INTO py_blogs(no,title) VALUES (%s,%s);",(i+1,titles[i])
	)
conn.commit()


cur.close()
conn.close()

