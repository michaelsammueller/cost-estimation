from cmd import *  # for importing cmd inputs
import os
import json
import pandas as pd
from calculation import ProjectEstimator


data = {}
files = []  # list for file selection


class UserInputs(Cmd):
    """Class to contain main terminal options by using the do_ commands to record user input"""

    def __init__(self):
        """Class to handle cli commands"""
        super().__init__()
        self.estimator = ProjectEstimator()

    def do_ext(self, *args):
        """Closes the program"""
        print("Program Terminated!")
        exit()

    def do_ld(self, *args):
        """displaying and loading the files in the directory"""

        global data, files  # accessing the global variables

        path = r"data"
        file_path = os.listdir(path)  # method for listing all the file in the project directory
        for file in file_path:
            print(file)  # show the files in the terminal
            files.append(file)  # adding the file in a list

        file_name_input = input("Please type a file name from the list above or type ext to terminate the program")

        if file_name_input in files:

            # syntax used to open json file
            with open(f'data/{file_name_input}', 'r') as file1:
                data = json.load(file1)
                #print(data)
                print("Json File Loaded")  # test if the file is loaded

        elif file_name_input == "ext":
            exit()

        else:
            print("File not in the directory!")

    def do_pd(self, *args):
        """ A function to  interpret and print .json files data"""
        global data

        # assigning the data dic a variable
        hardware = data['Hardware']
        software = data['Software']
        resources = data['Resources']

        # Using Pandas dataframe method to display the tables in the terminal
        hw_table = pd.DataFrame([[value for key, value in item.items()] for item in hardware],
                                columns=["Type", "Description", "Count", "Price", "Mfg. Cost", "Design Cost",
                                         "Coding Cost", "Testing Cost", "skill_1_needed", "skill_2_needed"])

        sw_table = pd.DataFrame([[value for key, value in item.items()] for item in software],
                                columns=["Type", "Description", "Count", "Price", "Mfg. Cost", "Design Cost",
                                         "Coding Cost", "Testing Cost", "lines_of_code",
                                         "skill_1_needed", "skill_2_needed",
                                         "skill_3_needed"])

        res_table = pd.DataFrame([[value for key, value in item.items()] for item in resources],
                                 columns=["role", "type", "count", "cost", "days", "skill_1", "skill_2", "skill_3"])

        print(20 * "-", " Hardware Components", 20 * "-")
        print(hw_table)
        print(20 * "-", " Software Components", 20 * "-")
        print(sw_table)
        print(20 * "-", " Resources", 20 * "-")
        print(res_table)

    def do_clc(self, *args):
        """A function for calculating the .json data using the calculation .py """

        self.estimator.clear()
        self.estimator.read_json_data(data)

        # gets calculation methods from calculator
        grand_total = self.estimator.total_system_cost()
        print(f"Grand_Total = {grand_total}")
        system_cost = self.estimator.cost_per_system()
        print(f"System_Cost = {system_cost}")
        cocomo_cost = self.estimator.cocomo_estimation("Organic")
        print(f"cocomo_cost = {cocomo_cost}")
        actual_staff_cost = self.estimator.total_staff_cost()
        print(f"Actual_Staff_Cost = {actual_staff_cost}")


def main_menu():
    print(10 * "=" + " " + "Synful Computing Cost Calculator:" + " " + 10 * "=")


def menu():
    """CLI Main Menu"""
    print(10 * "=" + " " + "Insert one of the following commands:" + " " + 10 * "=")
    print("""
    ld = Loads .json file in directory. 
    pd = previews current Hardware, Software Components and resources in the .json file 
    clc = calculates and previews total costs of Hardware, Software, and resources. 
    ext = Terminates program. 
    """)


main_menu()
menu()
UserInputs().cmdloop()
