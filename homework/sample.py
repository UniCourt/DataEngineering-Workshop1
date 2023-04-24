import requests
import csv
from bs4 import BeautifulSoup
response = requests.get("https://blog.python.org/")
soup = BeautifulSoup(response.content, 'html.parser')
title = soup.find_all("h1")
with open('res1.csv','w',newline='') as f:
	writer=csv.writer(f)
	writer.writerow(['column1','column2','column3'])
	for row in title:
		writer.writerow(row)

f.close()
lines=soup.find_all('p')
for line in lines:
	print(line.text)
