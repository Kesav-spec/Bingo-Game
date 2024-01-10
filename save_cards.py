from fpdf import FPDF
class BingoPDF(FPDF):

    def add_card(self,card,player_no):
        
        self.add_page()
        self.set_font("Arial", size=12)

        # Calculate the starting position to center the card on the page
        page_width = self.w
        # Assuming each cell is 20 units wide
        card_width = len(card) * 20  
        x_start = (page_width - card_width) / 2
        for i in card:
            self.ln()
        text = f"Card {player_no}"
        self.cell(20,10,str(text),align='C')
        self.ln()

        for row in card:
            self.set_x(x_start)
            for number in row:
                if str(number) == "":
                    self.cell(20,10,str('X'),border=1,align="C")
                else:
                    self.cell(20,10,str(number), border=1,align="C")
            self.ln()

def save_file(cards):

    pdf = BingoPDF()

    for i in range(len(cards)):
        pdf.add_card(cards[i].cards,i+1)

    pdf.output('./bingo_cards.pdf')

    
        


