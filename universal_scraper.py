import requests
from bs4 import BeautifulSoup

url = input("Enter website URL: ")

try:
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.find("h2").text)

    print("\n========== SCRAPING RESULT ==========")

    print("\nTitle:")
    print(soup.title.get_text(strip=True) if soup.title else "No title found")

    print("\nHeadings:")
    for heading in soup.find_all(["h1", "h2", "h3"]):
        text = heading.get_text(" ", strip=True)
        if text:
            print("-", text)

    print("\nParagraphs:")
    for paragraph in soup.find_all("p"):
        text = paragraph.get_text(" ", strip=True)
        if text:
            print("-", text)

    print("\nLinks:")
    for link in soup.find_all("a", href=True):
        print("-", link["href"])

except requests.RequestException as e:
    print("Error:", e)
