from bs4 import BeautifulSoup
import requests
import re

tagfind=re.compile("h2")
obj = requests.get('https://docs.docker.com/desktop/install/ubuntu/',timeout=5)
find = obj.content
soup = BeautifulSoup(find,'html.parser')
find2=soup.find_all(re.compile("h2"))
found=tagfind.search(find2)
found.group(0)




