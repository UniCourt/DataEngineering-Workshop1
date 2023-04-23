import requests
from bs4 import BeautifulSoup

r=requests.get('https://blog.python.org/')
soup=BeautifulSoup(r.content,'html.parser')
images_list=[]
images=soup.select('img')
for image in images:
	src=image.get('src')
	alt=image.get('alt')
	images_list.append({"src": src, "alt": alt})

for image in images_list:
	print(image)
