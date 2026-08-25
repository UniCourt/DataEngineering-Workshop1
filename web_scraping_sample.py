import requests
from bs4 import BeautifulSoup
import re

res = requests.get('https://www.lipsum.com/')
soup = BeautifulSoup(res.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
data = soup.find('div', id=re.compile(r"Panes"))
print(soup.find("h1").text)

question_list = []
answer_list = []
for row in data.find_all("div"):
    question_header = row.h2
    question_list.append(question_header.text)
    answer_string = ""
    parent_div_element = row.find_parent("div")
    all_p_tag_list = parent_div_element.find_all("p")
    for p_tag in all_p_tag_list:
        answer_string = answer_string + p_tag.text + "\n"
    answer_list.append(answer_string)

file = open("qn_and_answer.txt", "w")
for i in range(len(question_list)):
    file.write(question_list[i] + "\n" + answer_list[i] + "\n")
file.close()

print("The question and answer have been saved to qn_and_answer.txt file")


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
