try:
    f = open("non_existing_file.txt", "r")
    print(f.read())

    a=int(input("Enter number: "))
    b=int(input("Enter another number: "))
    print("Result:", a/b)

except FileNotFoundError:
    print("Error: File not found.")
except ZeroDivisionError:
    print("Error: Cannot divide by zero.")
except Exception as e:
    print("Some other error occurred:", e)
