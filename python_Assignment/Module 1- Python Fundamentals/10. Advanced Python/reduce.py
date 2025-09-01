from functools import reduce

nums=[1, 2, 3, 4, 5]

result=reduce(lambda a,b:a*b,nums)

print("Product of all numbers:",result)
