# Introduction to Webscraping.
<br />

## urllib2/requests:
   
### Request
<br />

```
Introduction: 
The requests module allows you to send HTTP requests using Python.
```
<br />

```
Important Methods:

    1)get(url,params,args)
            Sends a GET request to the specified url
    2)post(url,data,json,args)
            Sends a POST request to the specified url
    3)delete(url,args)
            Sends a DELETE request to the specified url
```    
> Explore [https://www.w3schools.com/python/module_requests.asp](https://www.w3schools.com/python/module_requests.asp)

<br />
     
```          
Example: Using GET
import requests
response_object = requests.get('https://www.lipsum.com/')
html = response_object.content
```      
<br />

### Urllib
<br />

```
Introduction:
It is a Python 3 package that allows you to access, and interact with, websites using their URL’s (Uniform Resource Locator).
It has several modules for working with URL’s.
```
<br />

```
Urllib.request
    Using urllib.request, with urlopen, allows you to open the specified URL.
Urllib.error
    This module is used to catch exceptions encountered from url.request
```
> Explore [https://www.geeksforgeeks.org/python-urllib-module/](https://www.geeksforgeeks.org/python-urllib-module/)

<br />

```
Example: 
import urllib.request
request_url = urllib.request.urlopen('https://www.lipsum.com/')
print(request_url.read())

```
<br />

## Beautifulsoup
<br />

```
Introduction:   
Beautiful Soup is a python package which allows us to pull data out of HTML and XML documents.

Beautiful Soup - Installation
pip install beautifulsoup4
```
<br />

```
Important Methods
                
find(name, attrs, recursive, string, **kwargs)

   scan the entire document to find only one result.

find_all(name, attrs, recursive, string, limit, **kwargs)

   You can use find_all to extract all the occurrences of a particular tag from the html

```
> Explore [https://www.crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

<br />

```
Example:
html = """
<html>
<head> <title> Beautiful Soup Example </title> </head>
</html>
"""

from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
print(soup.title)
```
<br />

## Regex
<br />

```
Introduction
The Python module re provides full support for Perl-like regular expressions in Python
```
<br />

```
   
Important methods

re.match(pattern, string, flags=0)

  The re.match function returns a match object on success, None on failure. We usegroup(num) or groups() function of the match object to get a matched expression

re.search(pattern, string, flags=0)

  The search() function searches the string for a match, and returns a Match object if there is a match.

re.findall(pattern, string, flags=0))

  function returns a list containing all matches.

re.sub(pattern,replace_string,string)

  The sub() function replaces the matches with the text of your choice

Metacharacters

        []	a set of a character
        .	 any character
        ^	start with
        $ 	end with
        * 	zero or more occurrences
        +	one or more occurrences
        ?	zero or one occurrences
        {}	exactly specified number of occurrence
        () 	capture a group
Important Special Sequences
        \w		Matches word characters.
        \W		Matches nonword characters.
        \s		Matches whitespace. Equivalent to [\t\n\r\f].
        \S	           Matches nonwhitespace	
        \d		Matches digits. Equivalent to [0-9].
        \D		Matches Nondigits
```
<br />

## Writing a script using the above packages and run it in Docker
<br />

```
Python Script: 
Filename: web_scraping_sample.py

import requests
from bs4 import BeautifulSoup
import re
res = requests.get('https://www.lipsum.com/')
soup = BeautifulSoup(res.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
data=soup.find(re.compile(r'div'),attrs={'id':"Panes"})
print(data.find("lorem"))
qes_list=[]
ans_list=[]
for row in data.findAll("div"):
    qes_list.append(row.h2.text)
    tempstring=""
    counter=0
    for i in row.findAll("p"):
        tempstring=tempstring+"\n"+i.text
    ans_list.append(tempstring)
tempstring=""
for i in range(len(qes_list)):
    tempstring=tempstring+"\n"+qes_list[i]+"\n"+ans_list[i]+"\n--------------------------------------------------------------------------------------------------\n\n"
    print(tempstring)
```
<br />

```
Creating a dockerfile:
Filename: Dockerfile
		
FROM python:3.10.2-alpine3.15
# Create directories  
RUN mkdir -p /root/workspace/src
COPY ./web_scraping_sample.py  /root/workspace/src
# Switch to project directory
WORKDIR /root/workspace/src
# Install required packages
RUN pip install --upgrade pip
RUN pip install requests bs4 html5lib
CMD ["web_scraping_sample.py"]
ENTRYPOINT ["python"]
```
<br />

```
Build docker image and run:

docker build --no-cache --network=host ./ -t simple_python
docker run --network=host simple_python
```