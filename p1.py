import requests
from bs4 import BeautifulSoup


import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="WebScrap",
    user="postgres",
    password="Lak@2002"
)
conn.autocommit = True
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS scrapeData(id SERIAL PRIMARY KEY, postDay VARCHAR, postHead VARCHAR, postBody VARCHAR, postAuthor VARCHAR);")


getUrl = requests.get('https://blog.python.org/')
recvHtml = getUrl.content

bsObj = BeautifulSoup(recvHtml,'html.parser')

pbar=""
for post in bsObj.find_all("div",class_="date-outer"):
	postVar=""
	date = post.find("h2",class_="date-header")
	dateVar = date.text
	

	main_head = post.find("h3",class_="post-title entry-title")
	headVar = main_head.text
	

	for content_body in post.find("div", class_="post-body entry-content"): 
		
		postVar = postVar+(content_body.text+"\n")
	
	author_name = post.find("span",class_="fn")
	authorVar = author_name.text
	

	cur.execute("INSERT INTO scrapeData (postDay,postHead,postBody,postAuthor) VALUES(%s,%s,%s,%s)",[dateVar,headVar,postVar,authorVar])
	
	pbar=pbar+"==="
	print(pbar)


print("Data Scraped Sucessfully and is stored in the Database")
cur.close()
conn.close()
