try:
    f = open("mydata.txt", "r")
    print(f.read())

except FileNotFoundError:
    print("Error: File does not exist.")
finally:
    try:
        f.close()
        print("File closed.")
    except:
        print("File was never opened.")
