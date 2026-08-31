import requests
from bs4 import BeautifulSoup
import re

res = requests.get('https://www.lipsum.com/')

soup = BeautifulSoup(res.content, 'html5lib')

data = soup.find(re.compile(r'div'), attrs={'id': "Panes"})

print(data.find("lorem"))

qes_list = []
ans_list = []

for row in data.findAll("div"):
    qes_list.append(row.h2.text)
    tempstring = ""
    for i in row.findAll("p"):
        tempstring = tempstring + "\n" + i.text
    ans_list.append(tempstring)

tempstring = ""

for i in range(len(qes_list)):
    tempstring = tempstring + "\n" + qes_list[i] + "\n" + ans_list[i]
    tempstring = tempstring + "\n--------------------------------------------------\n\n"
    print(tempstring)
