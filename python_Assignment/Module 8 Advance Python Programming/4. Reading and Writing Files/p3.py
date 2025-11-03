file = open("myfile.txt", "r")

data = file.read(10) 

print("Data read:", data)

position = file.tell()

print("Current cursor position:", position)

file.close()
