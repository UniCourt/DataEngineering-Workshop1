#Python script to list all titles from "blog.python.org/blog"
import requests
from bs4 import BeautifulSoup
import re

res = requests.get('https://blog.python.org/blog')
soup = BeautifulSoup(res.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
data = soup.find_all('h3', class_="text-base font-semibold leading-snug text-zinc-900 transition-colors group-hover:text-[#306998] dark:text-zinc-100 dark:group-hover:text-[#ffd43b]")
for row in data:
    print(row.text)
