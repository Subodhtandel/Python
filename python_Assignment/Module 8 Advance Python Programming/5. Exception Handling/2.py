try:
    a=float(input("Enter the first digit:"))
    b=float(input("ENter the secound Digit:"))
    print("Result:", a / b)

except ValueError:
    print("Invalid input! Please Enter The Numbers Only..")
except ZeroDivisionError:
    print("Cannot Divide by Zero.")
except Exception as e:
    print("Some other error occurred:", e)