# Main Graphical Interface file. this file will contain all the functions related to the application interface.

import tkinter as tk
from tkinter import *


class GuiMain:
    """Class for handling the interface settings and functions"""
    def __init__(self):
        self.root = tk.Tk()  # assigning the tkinter function to the variable "root" start the app
        self.root.title("Synful Computing Software")   # assigning title
        self.root.geometry('1080x300')  # assigning Window Size
        self.root.configure(bg='white')  # assigning Window Color
        self.root.iconbitmap('')    # adding an Icon next to the title
        menu = Menu(self.root)      # setting up a menu bar at the top
        self.root.config(menu=menu)

        # File option in Menu Bar
        file_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.root.quit)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # About option in Menu Bar
        about_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="About", command=self.root.quit)

        # Frames To organize widgets in windows
        self.top_frame = tk.Frame(self.root, bg='white')
        self.bot_frame = tk.Frame(self.root)
        self.top_frame.pack(), self.bot_frame.pack(side=TOP)

        # Text Labels
        self.top_label = tk.Label(self.top_frame,
                                  text="Synful Computing Cost Calculator Tool",
                                  font=("Helvetica bold", 15),
                                  bg='white',
                                  fg='grey')
        self.bot_label = tk.Label(self.top_frame,
                                  text="To see the existing calculated costs from .json data, please click 'Current',"
                                       "or click 'New' to select a new json file.",
                                  font=("Helvetica", 10),
                                  bg='white',
                                  fg='black')
        self.top_label.pack(padx=20, pady=20)
        self.bot_label.pack(padx=20, pady=20)

        # Buttons
        self.button_1 = tk.Button(self.bot_frame, text="New", padx=10, pady=5, height=2, width=10, bg='grey')
        self.button_1.grid(column=0, row=0)
        self.button_2 = tk.Button(self.bot_frame, text="Current", padx=5, pady=5, height=2, width=10, bg='grey')
        self.button_2.grid(column=1, row=0)

    def open_app(self):
        """Starts Tkinter"""
        self.root.mainloop()

    def new_calc(self):
        """ Function for attempting new calculation by selection json file """

    def existing_calc(self):
        """ Function for calculated by existing json file """

    def calculate(self):
        """Calculates total cost"""

    def export_json(self):
        """Calculates total cost"""

    def import_json(self):
        """Calculates total cost"""


start = GuiMain()
start.open_app()
