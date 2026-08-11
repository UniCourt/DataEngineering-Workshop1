#!/usr/bin/python

import requests
obj = requests.get('https://www.lipsum.com/')
response_object = requests.get('https://www.lipsum.com/')
html = response_object.content
print(html)
