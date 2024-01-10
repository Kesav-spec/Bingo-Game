import random
import math
import numpy as np

class Create_cards:
    def __init__(self,no_of_rows = 5,no_of_columns = 5):
        self.rows = no_of_rows
        self.columns = no_of_columns
        self.cards = []
        self.generate_cards()

    def generate_cards(self):
        number_range = 0
        cards = []
        range_ = self.columns * 15
        for i in range(self.columns):
            cards.append(random.sample(range(number_range + 1, number_range + math.floor(range_ / self.columns) + 1),
                                       k=self.rows))
            number_range += math.floor(range_ / self.columns)
        if self.columns == self.rows and (self.columns % 2 != 0):
            cards[int((self.rows - 1) / 2)][int((self.columns - 1) / 2)] = ''

        
        cards_array = np.array(cards)
        transposed_array = np.transpose(cards_array) 
        self.cards = transposed_array.tolist()

        #return list(map(list, zip(*cards)))