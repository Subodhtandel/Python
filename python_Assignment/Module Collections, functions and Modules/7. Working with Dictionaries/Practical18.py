text="programming"

char_count={}

for char in text:
    if char in char_count:
        char_count[char] += 1
    else:
        char_count[char] = 1

print("String:",text)
print("Character counts:",char_count)
