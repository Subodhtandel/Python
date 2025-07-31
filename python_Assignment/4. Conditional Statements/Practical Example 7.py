marks=int(input("Enter the marks:"))

if marks>=90:
    print("Grade A+")
elif marks>=80:
    print("Grade A")
elif marks>=70:
    print("Grade B")
elif marks>=60:
    print("Grade C")
elif marks>=50:
    print("Grade D")
elif marks>=40:
    print("Grade E")
else:
    print("\033[91mYou Are Fail!\033[0m")