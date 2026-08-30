import requests
import csv
from bs4 import BeautifulSoup
res=requests.get("https://blog.python.org/")
soup = BeautifulSoup(res.content, "html.parser")
titles = soup.find_all("h3")
titles_list=[]
count=1
for title in titles:
 d={}
 d['column1']=f'count'
 d['column2']=f'count{count}'
 d['column3']=title.text
 count+=1
 titles_list.append(d)
 filename='output2.csv'
with open(filename,'w',newline='') as f:
 writer = csv.DictWriter(f,['column1','column2', 'column3'])
 writer.writeheader()
 writer.writerows(titles_list)
f.close()

