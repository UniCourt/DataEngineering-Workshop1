"""import requests
from bs4 import BeautifulSoup
import re
import psycopg2

# Create connection to database
conn = psycopg2.connect(
    host="postgres_service",
    database="LipsumGenerator",
    user="postgres",
    password="admin")
cursor = conn.cursor()

res = requests.get('https://www.lipsum.com/')
soup = BeautifulSoup(res.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
data = soup.find(re.compile(r'div'), attrs={'id': "Panes"})
print(data.find("lorem"))

question_list = []
answer_list = []
for row in data.findAll("div"):
    question_list.append(row.h2.text)
    temp_string = ""
    counter=0
    for i in row.findAll("p"):
        temp_string = temp_string + "\n" + i.text
        answer_list.append(temp_string)
file = open("qn_ans_ans", "w")

for i in range(len(question_list)):
    cursor.execute("insert into qn_ans values(%s,%s)", (question_list[i], answer_list[i]))"""
    
    
#its for scraping 'https://blog.python.org/ ,this website. 
    
import requests
from bs4 import BeautifulSoup


import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="WebScrap",
    user="nick",
    password="Nishan@666"
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


print("Data Scraped and stored in the Database sucessfully")
cur.close()
conn.close()

