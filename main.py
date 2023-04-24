import requests
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

res = requests.get('https://blog.python.org/')
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
    cursor.execute("insert into qn_ans values(%s,%s)", (question_list[i], answer_list[i]))
