import requests
from bs4 import BeautifulSoup
import re

BASE = "https://blog.python.org"

HEADING_CLASS = ("text-base font-semibold leading-snug text-zinc-900 "
                 "transition-colors group-hover:text-[#306998] "
                 "dark:text-zinc-100 dark:group-hover:text-[#ffd43b]")
AUTHOR_CLASS = ("font-medium text-zinc-600 hover:text-[#306998] "
                "dark:text-zinc-300 dark:hover:text-[#ffd43b] transition-colors")


def fetch_page(url):
    res = requests.get(BASE + url)
    soup = BeautifulSoup(res.content, 'html5lib')

    headings = soup.find_all('h3', class_=HEADING_CLASS)
    authors = soup.find_all('a', class_=AUTHOR_CLASS, href=True)
    dates = soup.find_all('time')

    items = []
    for heading, author, date in zip(headings, authors, dates):
        items.append((heading.text.strip(), author.text.strip(), date.text.strip()))

    next_btn = soup.find("a", string=re.compile('Next'))
    next_url = next_btn['href'] if next_btn else None
    return items, next_url
