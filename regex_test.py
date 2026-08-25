import re

text = "My phone number is 9876543210"

match = re.match(r"My", text)
print(match.group() if match else None)

search = re.search(r"\d+", text)
print(search.group() if search else None)

numbers = re.findall(r"\d+", text)
print(numbers)

new_text = re.sub(r"\d+", "XXXXXXXXXX", text)
print(new_text)
