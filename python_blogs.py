import requests
from bs4 import BeautifulSoup
url = "https://blog.python.org/blog/"
response= requests.get(url)
html=response.content
soup = BeautifulSoup(html, 'html.parser')
for post in soup.find_all("article"):
    heading = post.find("h3")
    if heading:
        print("Heading:", heading.get_text(strip=True))
        date = post.find("time")
        if date:
            print("Date:", date.get_text(strip=True))
        author = date.find_previous("a") if date else None
        if author:
            print("Author:", author.get_text(strip=True))
        print("-------------------")
