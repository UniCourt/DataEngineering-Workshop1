# import requests
# from bs4 import BeautifulSoup
# import re
# res = requests.get('https://www.lipsum.com/')
# soup = BeautifulSoup(res.content, 'html5lib')
# data=soup.find(re.compile(r'div'),attrs={'id':"Panes"})
# print(data.find("lorem"))
# qes_list=[]
# ans_list=[]
# for row in data.findAll("div"):
#     qes_list.append(row.h2.text)
#     tempstring=""
#     counter=0
#     for i in row.findAll("p"):
#         tempstring=tempstring+"\n"+i.text
#     ans_list.append(tempstring)
# tempstring=""
# for i in range(len(qes_list)):
#     tempstring=tempstring+"\n"+qes_list[i]+"\n"+ans_list[i]+"\n--------------------------------------------------------------------------------------------------\n\n"
#     print(tempstring)

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Target URL containing the PDF links
page_url = "https://sample-files.com/documents/pdf/"

# Step 1: Fetch and parse the target webpage
response = requests.get(page_url)
response.raise_for_status()  # Check for HTTP request errors
soup = BeautifulSoup(response.text, 'html.parser')

# Step 2: Find all 'a' tags with href ending in '.pdf'
pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

# Step 3: Create a folder to store downloaded PDFs
os.makedirs("downloaded_pdfs", exist_ok=True)

# Step 4: Download each PDF found
for link in pdf_links:
    # Handle relative links by converting them to absolute URLs
    full_pdf_url = urljoin(page_url, link)
    
    # Extract the file name from the URL
    file_name = os.path.join("downloaded_pdfs", full_pdf_url.split("/")[-1])
    
    print(f"Downloading: {file_name}...")
    
    # Stream the PDF file download to save memory
    with requests.get(full_pdf_url, stream=True) as pdf_response:
        pdf_response.raise_for_status()
        with open(file_name, 'wb') as f:
            for chunk in pdf_response.iter_content(chunk_size=8192):
                f.write(chunk)

print("All downloads finished!")
