List1 = ["apple", "banana", "mango", "grapes", "kiwi"]
string = input("Enter the string to search: ")

for item in List1:
    if item==string:
        print("Found!")
        break
else:
    print("Not found.")
