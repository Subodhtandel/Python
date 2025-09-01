keys = ["name", "age", "course", "semester"]
values = ["Kiran", 20, "Computer Engineering", 3]

my_dict={}

for i in range(len(keys)):
    my_dict[keys[i]] = values[i]

print("Dictionary created from two lists:")
print(my_dict)
