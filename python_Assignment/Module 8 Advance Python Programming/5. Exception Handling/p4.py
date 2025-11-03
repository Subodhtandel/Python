try:
    f = open("test.txt", "r")
    print(f.read())
except FileNotFoundError:
    print("File not found.")
finally:
    try:
        f.close()
    except NameError:
        pass
