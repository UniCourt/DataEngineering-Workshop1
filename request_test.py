import requests

url = "https://www.lipsum.com/"

response = requests.get(url)

print(response.status_code)
print(response.content[:500])
