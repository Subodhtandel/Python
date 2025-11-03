import re

text = "Python programming is interesting."

match = re.search(r"programming", text)

if match:
    print("Word found at position:", match.start())
else:
    print("Word not found.")