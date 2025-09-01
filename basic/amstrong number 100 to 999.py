for num in range(100, 1000):
    sum = 0
    temp = num
    while temp > 0:
        digit = temp % 10
        sum += digit ** 3  # Since 3-digit numbers
        temp //= 10

    if sum == num:
        print(num)
