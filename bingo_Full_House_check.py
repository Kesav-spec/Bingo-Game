class Bingo_checker:

    def __init__(self, no_of_players, no_of_rows, no_of_columns,cards):
        self.players = no_of_players
        self.rows = no_of_rows
        self.columns = no_of_columns
        self.cards = cards
        self.num = 0
        self.collected_numbers = []
        self.full_house_flag = False
        self.bingo_flag = False
        self.bingo_count_flag = False
        self.full_house_count_flag = False

    def check_number_in_card(self, num):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.cards[i][j] == str(num):
                    self.cards[i][j] = 0
        return self.cards

    def bingo_check(self):
        # Row check for Bingo
        if not self.bingo_flag:
            for row in self.cards:
                if set(row) == {0} or set(row) == {0, ''}:
                    self.bingo_flag = True
                    self.bingo_count_flag = True

        # Column check for Bingo
        if not self.bingo_flag:
            for i in range(len(self.cards)):
                col = [self.cards[j][i] for j in range(len(self.cards))]
                if set(col) == {0} or set(col) == {0, ' '}:
                    self.bingo_flag = True
                    self.bingo_count_flag = True

        # Primary Diagonal Check for Bingo
        if not self.bingo_flag:
            if set([self.cards[i][i] for i in range(len(self.cards))]) == {0, ''}:
                self.bingo_flag = True
                self.bingo_count_flag = True

        # Secondary Diagonal Check for Bingo
        if not self.bingo_flag:
            if set([self.cards[i][(len(self.cards) - i - 1)] for i in range(len(self.cards))]) == {0,''}:
                self.bingo_flag = True
                self.bingo_count_flag = True

        return self.bingo_flag

    def full_house_check(self):
        card_sum = 0
        for i in range(len(self.cards)):
            for j in range(len(self.cards)):
                if self.cards[i][j] == '':
                    continue
                card_sum += int(self.cards[i][j])
        if card_sum == 0:
            self.full_house_flag = True
            self.full_house_count_flag = True

        return self.full_house_flag
    
    
    
        
