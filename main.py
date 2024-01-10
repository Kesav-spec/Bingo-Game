import base64
from io import BytesIO
import platform
import os
import webbrowser
from bingo_Full_House_check import Bingo_checker
from creating_Bingo_cards import Create_cards
from random_number_generator import RandomNumber
from graph_plot import GraphPlot
from PIL import Image
import save_cards as sc
import copy

import tkinter as tk
from tkinter import OptionMenu, StringVar, messagebox

class GameGUI:

    #GUI Initiation
    def __init__(self,master):
        self.master = master
        self.master.title("Bingo Game")
        self.master.config(padx=20, pady=20)
        self.master.minsize(width=500, height=300)

        self.Label = tk.Label(text="BINGO!", font=("Arial", 24, "italic"))
        self.Label.grid(row=0, column=0, columnspan=5)

        self.num_players_label = tk.Label(self.master, text="Number of Players:")
        self.num_players_label.grid(row=2, column=0)

        self.num_players_entry = tk.Entry(self.master)
        self.num_players_entry.insert(0, 50)
        self.num_players_entry.grid(row=2,column=1)

        self.num_simulations_label = tk.Label(self.master, text="Number of Simulations:")
        self.num_simulations_label.grid(row=2,column=3)

        self.num_simulations_entry = tk.Entry(self.master)
        self.num_simulations_entry.insert(0,100)
        self.num_simulations_entry.grid(row=2,column=4)

        self.nums_to_be_called = tk.Label(self.master, text="Numbers to Call :")
        self.nums_to_be_called.grid(row=4,column=0)

        self.numbers_range_to_call = tk.Entry(self.master)
        self.numbers_range_to_call.insert(0, 75)
        self.numbers_range_to_call.grid(row=4,column=1)


        self.matrix_size = tk.Label(self.master,text="Select size of Cards :")
        self.matrix_size.grid(row=4,column=3)

        self.menu= StringVar()
        self.menu.set("Select Any Size of matrix")

        #Create a dropdown Menu
        self.drop= OptionMenu(self.master, self.menu,"5x5","7x7")
        self.drop.grid(row=4,column=4)

        self.is_ok = True
        self.num_players = 0
        self.matrix_length = 0
        self.num_simulations_ = 0

        self.exit_button = tk.Button(self.master,text="Quit",command=self.quit)
        self.exit_button.grid(row=10,column=2)

        self.play_button = tk.Button(self.master, text="Play Bingo", command=self.play_bingo)
        self.play_button.grid(row=9,column=2)

        self.Report_menu= StringVar()
        self.Report_menu.set("Select the report to check")

        self.Report_drop= OptionMenu(self.master, self.Report_menu,'CDF_Graph','Histogram','Bingo_Details','Full_house_Details')
        self.Report_drop.grid(row=8,column=2)

        self.view_Graph = tk.Button(self.master,text="ViewReport",command=self.open_graph)
        self.view_Graph.config(state=tk.DISABLED)
        self.view_Graph.grid(row=8,column=3)

        self.view_cards = tk.Button(self.master,text="ViewCards",command=self.open_cards)
        self.view_cards.config(state=tk.DISABLED)
        self.view_cards.grid(row=7,column=2)

        # Create a label to display the image
        self.label = tk.Label(self.master)
        self.label.grid(row=10, column=3, columnspan=5)




    def play_bingo(self):
        # Input Validation
        try:
            self.num_players = int(self.num_players_entry.get())
            self.num_simulations_ = int(self.num_simulations_entry.get())
            self.matrix_length = int(self.menu.get().split('x')[0])
            self.range_of_numbers_to_call = int(self.numbers_range_to_call.get())

            if self.num_players < 1 or self.num_simulations_ < 1:
                messagebox.showerror("Error", "Number of players and simulations must be greater than zero.")
                self.is_ok = False
            if self.num_simulations_ >=1000:
                self.is_ok = messagebox.askyesno(message = f"You have given simulations of number {self.num_simulations_} it will take some time to generate your results Do you want to continue ?")
                if not self.is_ok:
                    self.is_ok = False
            if type(self.num_players) != int :
                messagebox.showerror(f"You have entered {self.num_players}, you must provide a provide a number instead")
                self.is_ok = False
            if type(self.num_simulations_) != int :
                messagebox.showerror(f"You have entered {self.num_simulations_}, you must provide a provide a number instead")
                self.is_ok = False
            if type(int(self.menu.get()[0])) != int:
                messagebox.showerror("Please Pick the size of the cards from the Drop Down!")
                self.is_ok = False
            if self.range_of_numbers_to_call <= 30 and self.range_of_numbers_to_call >= 1:
                self.is_ok = messagebox.askyesno(message=f"You have entered the value {self.range_of_numbers_to_call} there is high chance of not encountering a bingo . Do you want to still continue?")
                if not self.is_ok:
                    self.is_ok = False
            if type(self.range_of_numbers_to_call) != int:
                messagebox.showerror(f"You have entered {self.range_of_numbers_to_call}, you must provide a provide a number instead")   
                self.is_ok = False   
            if self.range_of_numbers_to_call <= 0:
                messagebox.showerror(f"You have Entered {self.range_of_numbers_to_call}, Please Enter valid positive number in the cell Numbers to call")      
                self.is_ok = False  
            if self.range_of_numbers_to_call > 75:
                messagebox.showerror("Numbers to call should not go be greater than 75")     
                self.is_ok = False    
            if type(int(self.range_of_numbers_to_call)) != int:
                messagebox.showerror("Please provide number in numbers to call column (1-75)")
                self.is_ok = False       
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for players and simulations and check whether the  matrix length is selected or not. .")
            self.is_ok = False

        #If data is valid proceed for simmulation
        
        if self.is_ok:
            self.view_Graph.config(state=tk.DISABLED)
            self.view_cards.config(state=tk.DISABLED)
                
            cards = {}
            bingo_cards = {}
            bingo_encounter_for_bingo = []
            bingo_encounter_for_full_house = []
            bingo_encounter_for_bingo_raw = []
            bingo_encounter_for_full_house_raw = []

            #creating cards with number of players provided
            for i in range(self.num_players):
                bingo_cards[i] = Create_cards(no_of_rows=self.matrix_length,no_of_columns=self.matrix_length)
            
            #saving the generated cards.
            sc.save_file(bingo_cards)
            
            #running the cards for the simmulations given
            count = 0
            while count < self.num_simulations_:
                for i in range(self.num_players):
                    cards[i] = Bingo_checker(no_of_players=self.num_players, no_of_rows=self.matrix_length, no_of_columns=self.matrix_length,cards = copy.deepcopy(bingo_cards[i].cards))

                #Initiate Random Number Class
                random_number = RandomNumber()

                game = True
                full_house_count = 0
                bingo_data = [0 for i in range(self.range_of_numbers_to_call)]
                full_house_data = [0 for i in range(self.range_of_numbers_to_call)]
                bingo_data_raw = [0 for i in range(self.range_of_numbers_to_call)]
                full_house_data_raw = [0 for i in range(self.range_of_numbers_to_call)]
                bingo_count_per_number = 0
                full_house_per_number = 0
                j = 0
                iter = 0
                # Game 
                while game:
                    bingo_count_per_number_raw = 0
                    full_house_count_per_number_raw = 0
                    iter +=1
                    if iter <= self.range_of_numbers_to_call:
                        number_called = random_number.generate_random_number()
                        for i in range(len(cards)):
                            cards[i].check_number_in_card(num=number_called)
                            if not cards[i].bingo_flag:
                                cards[i].bingo_check()
                            if not cards[i].full_house_flag:
                                if cards[i].full_house_check():
                                    full_house_count += 1
                                    full_house_count_per_number_raw+=1
                            if cards[i].bingo_count_flag:
                                bingo_count_per_number+=1
                                bingo_count_per_number_raw +=1
                                cards[i].bingo_count_flag = False
                            if cards[i].full_house_count_flag:
                                full_house_per_number +=1
                                cards[i].full_house_count_flag = False
                            if full_house_count == int(self.num_players):
                                game = False
                        # storing data to plot CDF and histogram
                        bingo_data[j] = bingo_count_per_number
                        full_house_data[j] = full_house_per_number
                        bingo_data_raw[j] = bingo_count_per_number_raw
                        full_house_data_raw[j] = full_house_count_per_number_raw
                    # if numbers range is given less than 75 game will end when the range is met.
                    if(len(bingo_data)==j+1):
                        game = False

                    j+=1
                    # For CDF graph if full house of all cards occured before 75 numbers being called the remaining numbers will be swapped with corresponding values. 
                    if not game:
                        if iter < 75 and self.range_of_numbers_to_call==75:
                            for k in range(len(bingo_data)-iter):
                                temp_1 = bingo_data[iter-1]
                                temp_2 = full_house_data[iter-1]
                                bingo_data[iter+k] = temp_1
                                full_house_data[iter+k] = temp_2
                count+=1
                bingo_encounter_for_bingo.append(bingo_data)
                bingo_encounter_for_full_house.append(full_house_data)
                bingo_encounter_for_bingo_raw.append(bingo_data_raw)
                bingo_encounter_for_full_house_raw.append(full_house_data_raw)

            #Graph Generation
            graph = GraphPlot(bingo_data_cdf=bingo_encounter_for_bingo,full_house_data_cdf=bingo_encounter_for_full_house,bingo_data_raw=bingo_encounter_for_bingo_raw,full_house_data_raw=bingo_encounter_for_full_house_raw)
            graph.do_np_transform()
            graph.plot_histogram()
            # Enabling buttons to view results
            self.view_Graph.config(state=tk.NORMAL)
            self.view_cards.config(state=tk.NORMAL)

    def quit(self):
        self.master.destroy()

    # Display Graph in a webBrowser
    def open_graph(self):
        platform_name = platform.system()
        images_ = ['CDF_Graph','Histogram']
        details = ['Bingo_Details','Full_house_Details']
        if self.Report_menu.get() in images_:
            file_path = f"./{self.Report_menu.get()}.png"
        if self.Report_menu.get() in details:
            file_path = f"./{self.Report_menu.get()}.html"

        if platform_name == 'Darwin':
            if file_path and self.Report_menu.get() in images_:
                # Open the image using PIL
                image = Image.open(file_path)
                # Converts the image to a data URL
                buffered = BytesIO()
                image.save(buffered, format="PNG")  # Change the format as needed
                image_data = base64.b64encode(buffered.getvalue()).decode("utf-8")
                data_url = f"data:image/png;base64,{image_data}"

                # Open the data URL in the default web browser
                webbrowser.open_new_tab(data_url)
            if file_path and self.Report_menu.get() in details:
                webbrowser.open_new_tab(f"file://{os.path.abspath(file_path)}")

        if platform_name == 'Windows':
            if file_path and self.Report_menu.get() in images_:
                # Open the image using PIL
                image = Image.open(file_path)
                # Converts the image to a data URL
                buffered = BytesIO()
                image.save(buffered, format="PNG")  # Change the format as needed
                image_data = base64.b64encode(buffered.getvalue()).decode("utf-8")
                data_url = f"data:image/png;base64,{image_data}"
                
                # Converting the data into HTML Content for viewing the graphs
                html_content = f'<html><body><img src="{data_url}"></body></html>'
                html_file_path = "temp_image.html"
                with open(html_file_path, "w") as html_file:
                    html_file.write(html_content)

                # Open the HTML file in the default web browser
                webbrowser.open_new_tab(f"file://{os.path.abspath(html_file_path)}")
            if file_path and self.Report_menu.get() in details:
                webbrowser.open_new_tab(f"file://{os.path.abspath(file_path)}")


    #Open cards gnerated as pdf in webbrowser
    def open_cards(self):
        platform_name = platform.system()
        file_path = './bingo_cards.pdf'

        if platform_name == 'Darwin':
            if file_path: 
                with open(file_path, 'rb') as file:
                    encoded_pdf = base64.b64encode(file.read()).decode('utf-8')
                    url = f"data:application/pdf;base64,{encoded_pdf}"
                    webbrowser.open(url, new=2)
        if platform_name == 'Windows':
            if file_path: 
                with open(file_path, 'rb') as file:
                    webbrowser.open_new_tab(f"file://{os.path.abspath(file_path)}")


if __name__=="__main__":
    window = tk.Tk()
    gui = GameGUI(window)
    window.mainloop()




    

    

