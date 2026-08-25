import requests
from bs4 import BeautifulSoup

URL = 'https://nitte.edu.in/'
headers = {
    'User-Agent': 'Mozilla/5.0'
}


print(f"Fetching data from {URL}...\n")
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Target .rightItems2 where Sustainable Nitte lives
section = soup.find('div', class_='rightItems2')

if section:
    # Extract Heading
    heading = section.find('h2', class_='head').get_text(strip=True)
    
    # Extract Paragraph
    paragraph = section.find('p').get_text(strip=True)
    
    # Extract Read More Link
    link_tag = section.find('a', class_='btn-one-full')
    link_url = link_tag['href'] if link_tag else 'No link'

    print(f"=== {heading} ===\n")
    print(f"{paragraph}\n")
    print(f"Read More Link: {link_url}\n")

    # Save to file
    with open('sustainable_nitte.txt', 'w', encoding='utf-8') as f:
        f.write(f"Heading: {heading}\n\nParagraph:\n{paragraph}\n\nLink: {link_url}\n")
    
    print("Result successfully saved to 'sustainable_nitte.txt'!")
else:
    print("Could not find the Sustainable Nitte section.")
