import requests

url = "https://pdfobject.com/pdf/sample.pdf"

response = requests.get(url)

print("Status code:", response.status_code)

with open("sample.pdf", "wb") as file:
    file.write(response.content)

print("PDF downloaded successfully!")
