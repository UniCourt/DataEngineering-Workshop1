import requests
from bs4 import BeautifulSoup
import os

n = int(input("How many PDFs to download? "))

url = "https://sample-files.com/documents/pdf/"
soup = BeautifulSoup(requests.get(url).text, "html.parser")
os.makedirs("pdfs", exist_ok=True)

count = 0

for a in soup.find_all("a", href=True):
    if ".pdf" in a["href"].lower():
        link = a["href"]

        if not link.startswith("http"):
            link = "https://sample-files.com" + link

        name = link.split("/")[-1]
        data = requests.get(link).content

        with open("pdfs/" + name, "wb") as f:
            f.write(data)

        print("Downloaded:", name)
        count += 1

        if count == n:
            break
