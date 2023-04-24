import requests
import csv
from bs4 import BeautifulSoup
res=requests.get("https://blog.python.org/")
soup = BeautifulSoup(res.content, "html.parser")
titles = soup.find_all("h1")
with open('output.csv','w',newline='') as f:
 writer = csv.writer(f)
 writer.writerow(['column 1','column 2','column 3'])
 for row in titles:
   writer.writerow(row)
f.close()
