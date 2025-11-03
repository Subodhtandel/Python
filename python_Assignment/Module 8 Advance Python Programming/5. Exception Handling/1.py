try:
    a=float(input("Enter the first digit:"))
    b=float(input("ENter the secound Digit:"))
    op=input("Enter the Operators(+,-,*,/):")
   
    if op == '+':
        print("Result:", a + b)
    elif op == '-':
        print("Result:", a - b)
    elif op == '*':
        print("Result:", a * b)
    elif op == '/':
        print("Result:", a / b)
    else:
        print("Invalid operator.")

except ValueError:
    print("Invalid input! Please Enter The Numbers Only..")
except ZeroDivisionError:
    print("Cannot Divide by Zero.")