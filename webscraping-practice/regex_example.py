import re

text = "My phone number is 9876543210 and my PIN is 1234"

# search()
print(re.search(r"\d+", text))

# findall()
print(re.findall(r"\d+", text))

# match()
print(re.match(r"My", text))

# sub()
print(re.sub(r"\d+", "NUMBER", text))
