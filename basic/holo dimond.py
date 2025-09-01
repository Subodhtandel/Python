n = 5  # Change this for bigger diamonds

# Upper half
for i in range(n):
    for j in range(n - i - 1):
        print(" ", end="")
    for j in range(2 * i + 1):
        if j == 0 or j == 2 * i:
            print("*", end="")
        else:
            print(" ", end="")
    print()

# Lower half
for i in range(n - 2, -1, -1):
    for j in range(n - i - 1):
        print(" ", end="")
    for j in range(2 * i + 1):
        if j == 0 or j == 2 * i:
            print("*", end="")
        else:
            print(" ", end="")
    print()
