class IntegerListIterator:
    def __init__(self, integer_list):
        self.integer_list=integer_list
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index<len(self.integer_list):
            value=self.integer_list[self.index]
            self.index += 1
            return value
        else:
            raise StopIteration

numbers = [10, 20, 30, 40, 50]
custom_iterator = IntegerListIterator(numbers)

print("Iterating over the list using custom iterator:")
for num in custom_iterator:
    print(num)