import re

text = "Python is powerful."

match = re.match(r"Python", text)

if match:
    print("Word matched at the beginning of the string.")
else:
    print("No match found.")