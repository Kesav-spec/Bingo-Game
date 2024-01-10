import random
class RandomNumber:

    def __init__(self):
        self.collected_numbers = []
        self.numbers_range = [i for i in range(1,76)]

    

    def generate_random_number(self):
        num = random.choice(self.numbers_range)
        if num in self.numbers_range:
            self.numbers_range.remove(num)
            self.collected_numbers.append(num)
        return num
