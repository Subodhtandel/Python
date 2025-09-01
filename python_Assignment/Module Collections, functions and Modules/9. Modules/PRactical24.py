import random

rand_num = random.randint(1, 100)
print("Random Number (1-100):", rand_num)

print("\nFive Random Numbers between 1 and 100:")
for i in range(5):
    print(random.randint(1, 100))
