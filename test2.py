import urllib.request
request_url = urllib.request.urlopen('https://www.lipsum.com/')
print(request_url.read())

