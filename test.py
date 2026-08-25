import requests
response_object = requests.get('https://www.lipsum.com/')
html = response_object.content
print(html)
