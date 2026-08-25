import requests
from bs4 import BeautifulSoup

url = "https://nitte.edu.in/nmamit/department-computer-science.php"

res = requests.get(url)

soup = BeautifulSoup(res.content, "html5lib")

faculty_section = soup.find("section", id="Faculty")

faculty_cards = faculty_section.find_all("div", class_="leadership-box")

for card in faculty_cards:
    name = card.find("h3")
    designation = card.find("p")

    print("Name:", name.get_text(strip=True))
    print("Designation:", designation.get_text(strip=True))


file = open("faculty.txt", "w")

for card in faculty_cards:
    name = card.find("h3").get_text(strip=True)
    designation = card.find("p").get_text(strip=True)

    print("Name:", name)
    print("Designation:", designation)
    print()

    file.write("Name: " + name + "\n")
    file.write("Designation: " + designation + "\n")
    file.write("-----------------------------\n")

file.close()

print("Faculty data saved to faculty.txt")