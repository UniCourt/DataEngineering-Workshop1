# import requests
# response_object = requests.get('https://www.lipsum.com/')
# html = response_object.content

# print(html)


import requests
from bs4 import BeautifulSoup

res = requests.get("https://en.wikipedia.org/wiki/Google")

soup = BeautifulSoup(res.content, "html5lib")

data = soup.find("div", id="Panes")

qes_list = []
ans_list = []

for row in data.find_all("div"):
    heading = row.find("h2")

    if heading:
        qes_list.append(heading.get_text(strip=True))

        tempstring = ""

        for p in row.find_all("p"):
            tempstring += "\n" + p.get_text(strip=True)

        ans_list.append(tempstring)

for i in range(len(qes_list)):
    print(qes_list[i])
    print(ans_list[i])
    print("-" * 100)