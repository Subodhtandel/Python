num = int(input("Enter a number: "))
power = len(str(num))

total = 0
temp = num

while temp > 0:
    digit = temp % 10
    total += digit ** power
    temp //= 10

if total == num:
    print("Armstrong number")
else:
    print("Not an Armstrong number")