from cmd import *  # for importing cmd inputs
import os
import json
import pandas as pd

data = {}
files = []  # list for file selection


class UserInputs(Cmd):
    """Class to contain main terminal options by using the do_ commands to record user input"""

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
                print("Json File Loaded")  # test if the file is loaded

        elif file_name_input == "ext":
            exit()

        else:
            print("File not in the directory!")

    def do_pd(self, *args):
        """ A function to  interpret .json files """
        global data

        hardware = data['Hardware']
        software = data['Software']
        resources = data['Resources']
        print(hardware)

        table = pd.DataFrame([[key] + list(value) for key, value in hardware.items()],
                             columns=["Type", "Description", "Count", "Price", "Mfg. Cost", "Design Cost",
                                      "Coding Cost", "Testing Cost", "Total"])

        print(table)

        # # The next step is to iterate over the data in the Json file to assign values to the tree nodes.
        # j_data = file1["data"]  # to iterate on the number of data present in the json file.
        # print(data_len)
        # main_root = data['root']['name']  # storing the name of the root node
        # node_names = list(data.keys())  # converting all the keys in the json to iterable list
        # hardware = data["Hardware"]
        # software = data["Software"]


def main_menu():
    print(10 * "=" + " " + "Synful Computing Cost Calculator:" + " " + 10 * "=")


def menu():
    """CLI Main Menu"""
    print(10 * "=" + " " + "Insert one of the following commands:" + " " + 10 * "=")
    print("""
    ld = Loads .json file in directory. 
    pd = previews current Hardware, Software Components and resources in the .json file 
    clc = calculates and previews total costs of Hardware, Software, and resources. 
    edt = edits json data for adding new components and resources. Can also modify costs. 
    exp = Exports modified data to a new .json file
    ext = Terminates program. 
    """)


main_menu()
menu()
UserInputs().cmdloop()
