# Main Graphical Interface file. this file will contain all the functions related to the application interface.
import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk, messagebox
import json
from calculation import ProjectEstimator


class GuiMain:
    """Class for handling the interface buttons, frames, fields and functions"""

    def __init__(self):
        # Initializing tkinter function to the variable "root" to start the app, and setting title and display settings.
        self.root = tk.Tk()
        self.root.title("Synful Computing Cost Calculator Tool")
        self.root.geometry('1400x720')
        self.root.configure(bg='white')
        self.frame_top = tk.Frame(self.root, bg='white')
        self.frame_top.pack(side=TOP)
        self.frame_bot = tk.Frame(self.root, bg='white')
        self.frame_bot.pack(pady=10, side=BOTTOM)

        # Initializing Calculation.py
        self.estimator = ProjectEstimator()

        # Initializing click events
        self.root.bind('<ButtonRelease-1>', self.table_select)
        self.root.bind('<Button-3>', self.clear_selection)

        # Initializing .json data set
        self.json_data = {}

        # table/tree viewer by tkinter to display data from .json
        self.table_view = ttk.Treeview(self.root, columns='value', selectmode='browse')
        self.table_view.heading('#0', text='Component')
        self.table_view.heading('value', text='Value')
        self.table_view.pack(expand=True, fill=tk.BOTH)



        # Event binding for table/treeview selection
        self.root.bind('<ButtonRelease-1>', self.table_select)

        # Buttons
        self.upload_button = tk.Button(self.frame_bot, text="Upload'.JSON'", padx=5, pady=5, height=1, width=20,
                                       bg='grey',
                                       command=lambda: self.select_json())
        self.upload_button.grid(row=0, column=4, padx=5)
        self.edit_button = tk.Button(self.frame_bot, text='Edit', padx=5, pady=5, height=1, width=15,
                                     command=lambda: self.edit())
        self.edit_button.grid(row=0, column=5, padx=5)
        self.add_button = tk.Button(self.frame_bot, text='Add', padx=5, pady=5, height=1, width=15,
                                    command=lambda: self.add())
        self.add_button.grid(row=0, column=6, padx=5)
        self.delete_button = tk.Button(self.frame_bot, text='Delete', padx=5, pady=5, height=1, width=15,
                                       command=lambda: self.delete())
        self.delete_button.grid(row=0, column=7, padx=5)

        self.save_button = tk.Button(self.frame_bot, text='Save', padx=5, pady=5, height=1, width=15,
                                     command=lambda: self.save())
        self.save_button.grid(row=0, column=8, padx=5)
        self.calculate_button = tk.Button(self.frame_bot, text='Calculate', padx=5, pady=5, height=1, width=15,
                                          command=lambda: self.calculate_data())
        self.calculate_button.grid(row=0, column=9, padx=5)

        # Top Menu Bar
        menu = Menu(self.root)
        self.root.config(menu=menu)
        file_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=lambda: self.select_json())
        file_menu.add_command(label="New", command=lambda: self.table_clear())
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="About", command=lambda: self.about_window())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        # Input field to change .json values
        self.key_label = tk.Label(self.frame_bot, text='KEY COMPONENT', bg='White')
        self.key_label.grid(row=0, column=0, padx=5)
        self.key_entry = tk.Entry(self.frame_bot)
        self.key_entry.grid(row=0, column=1, padx=5)

        self.value_label = tk.Label(self.frame_bot, text='VALUES', bg='White')
        self.value_label.grid(row=0, column=2, padx=5)
        self.value_entry = tk.Entry(self.frame_bot)
        self.value_entry.grid(row=0, column=3, padx=5)

        # Calc Preview.
        self.grand_total_label = tk.Label(self.frame_bot, text='GRAND TOTAL(2000)', bg='White', fg='Green')
        self.grand_total_label.grid(row=1, column=0, padx=5, pady=20)
        self.grand_total_entry = tk.Entry(self.frame_bot)
        self.grand_total_entry.grid(row=1, column=1, padx=5, pady=20)
        self.cost_system_label = tk.Label(self.frame_bot, text='SYSTEM COST', bg='White', fg='Green')
        self.cost_system_label.grid(row=1, column=2, padx=5, pady=20)
        self.cost_system_entry = tk.Entry(self.frame_bot)
        self.cost_system_entry.grid(row=1, column=3, padx=5, pady=20)
        self.tsc_cocomo_label = tk.Label(self.frame_bot, text='COCOMO COST', bg='White', fg='Green')
        self.tsc_cocomo_label.grid(row=1, column=4, padx=5, pady=20)
        self.tsc_cocomo_entry = tk.Entry(self.frame_bot)
        self.tsc_cocomo_entry.grid(row=1, column=5, padx=5, pady=20)
        self.atsc_label = tk.Label(self.frame_bot, text='ACTUAL STAFF COST (GBP)', bg='White', fg='Green')
        self.atsc_label.grid(row=1, column=6, padx=5, pady=20)
        self.atsc_entry = tk.Entry(self.frame_bot)
        self.atsc_entry.grid(row=1, column=7, padx=5, pady=20)

    def about_window(self):
        about_window = messagebox.showinfo("About", " Welcome to the Synful Computing Cost Calculator App "
                                                    "\n(UOE / Group 3)"
                                                    "\n _________________________________________________"
                                                    "\nUpload Json = To preview data in Table View"
                                                    "\nNew = To clear table and add new data in the Table View"
                                                    "\nSave = Save data to a new Json file")

    def open_app(self):
        """Starts Tkinter"""
        self.root.mainloop()

    def select_json(self):
        """Function for uploading .json file to the system"""

        # step 1 for locating json file using tkinter method.
        json_file = filedialog.askopenfilename(
            initialdir="/",
            title="Upload .Json",
            filetypes=((".json files", "*.json"), ("All files", "*.*")), )

        # step 1.5 clear table if it already exists
        self.table_clear(True)

        # step 2 loading data from .json
        with open(json_file, 'r') as file1:
            self.json_data = json.load(file1)
            self.table_fill('', self.json_data)

            file_path = file1.name
            last_slash_index = file_path.rfind("/")
            file_name = file_path[last_slash_index + 1:]
            confirmed = messagebox.showinfo("File Loaded", f"JSON file '{file_name}' loaded successfully.")

    def table_fill(self, key, value, parent=""):
        """ Function for adding data to the table tree viewer """
        # insuring item is a dict or list then allocating the values
        if isinstance(value, dict):
            parent_id = self.table_view.insert(parent, 'end', text=key, open=True,)

            for key, value in value.items():
                self.table_fill(key, value, parent_id)
        elif isinstance(value, list):
            parent_id = self.table_view.insert(parent, 'end', text=key, open=True)

            for i, item in enumerate(value):
                self.table_fill(str(i), item, parent_id)
        else:
            self.table_view.insert(parent, 'end', text=key, values=(value,))


    def table_clear(self, skip=False):
        """ Function for clearing all the data in table  """

        if not skip:
            confirmed = messagebox.askyesno("confirmation", "This will clear all the table data. continue?")

        # Delete all items from the tabl/treeview
        self.table_view.delete(*self.table_view.get_children())
        # Clear the JSON data
        self.json_data = {}

    def table_select(self, event):
        """ Function for adding the selected data from the table to the fields """
        # selecting data items based clicking on the table using ttk method
        if event.num == 1:
            # Get the selected items from the table
            selected_item = self.table_view.selection()

            # Check if there is any selected item
            if selected_item:
                # Collecting the key and value from the selected data from the table to the corresponding fields
                item = self.table_view.item(selected_item)
                key = item['text']
                value = item['values'][0] if item['values'] else ''

                self.key_entry.delete(0, tk.END)
                self.key_entry.insert(0, key)
                self.value_entry.delete(0, tk.END)
                self.value_entry.insert(0, value)
        else:
            # Left mouse button wasn't clicked, clear the selection
            self.table_view.selection_remove(self.table_view.selection())

    def clear_selection(self, event):
        """Function to clear the selection in the Treeview"""
        self.table_view.selection_remove(self.table_view.selection())
        self.value_entry.delete(0, tk.END)
        self.key_entry.delete(0, tk.END)


    def edit(self):
        """ Function for editing the selected data from input fields """
        selected_item = self.table_view.selection()
        if selected_item:
            item = self.table_view.item(selected_item)
            key = item['text']
            new_value = self.value_entry.get()
            try:
                new_value = json.loads(new_value)
            except json.JSONDecodeError:
                pass  # If the input is not a valid JSON, keep it as a string

            # Update the table or treeview
            self.table_view.item(selected_item, values=(new_value,))

            parent_id = self.table_view.parent(selected_item)
            grandparent_id = self.table_view.parent(parent_id)
            index = int(self.table_view.item(parent_id)["text"])
            kind = self.table_view.item(grandparent_id)["text"]

            self.json_data[kind][index][key] = new_value

    def add(self):
        """ Function for adding keys and values to the table """
        new_key = self.key_entry.get()
        new_value = self.value_entry.get()
        try:
            new_value = json.loads(new_value)
        except json.JSONDecodeError:
            pass  # If the input is not a valid JSON, keep it as a string

        # Insert new key-value pair into the treeview
        parent_item = self.table_view.selection()[0] if self.table_view.selection() else ''
        self.table_view.insert(parent_item, 'end', text=new_key, values=new_value)
        # Update the JSON data
        self.update(new_key, new_value)

    def update(self, key, new_value):
        """ Function for updating the added key and values to the table"""

        # Update the JSON data with the new value
        keys = key.split('.')
        data = self.json_data

        for k in keys[:-1]:
            if isinstance(data, dict):
                data = data.get(k, {})
            elif isinstance(data, list):
                try:
                    k = int(k)
                    data = data[k]
                except (ValueError, IndexError):
                    # Handle invalid index or key
                    return

        last_key = keys[-1]
        if isinstance(data, dict):
            data[last_key] = new_value
        elif isinstance(data, list):
            try:
                last_key = int(last_key)
                data[last_key] = new_value
            except (ValueError, IndexError):
                # Handle invalid index
                return

    def delete(self):
        selected_item = self.table_view.selection()
        if selected_item:
            key = self.table_view.item(selected_item)['text']
            parent_item = self.table_view.parent(selected_item)

            confirmed = messagebox.askyesno("Confirmation", f"Are you sure you want to delete '{key}'?")
            if confirmed:
                # Delete item from table/treeview
                self.table_view.delete(selected_item)

    def save(self):
        """ Function for saving the modified data to a new Json file """
        if not self.json_data:
            confirmed = messagebox.showinfo("Error", "No JSON data to save")
            print("No JSON data to save.")
            return

        # Open a file dialog to save the changes to a JSON file
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            # Save the changes back to the selected file
            with open(file_path, 'w') as file:
                json.dump(self.json_data, file, indent=2)
            confirmed = messagebox.showinfo("File Saved", f"JSON file '{file}' Saved successfully.")
            print("Changes saved to", file_path)

    def calculate_data(self):
        """ Function for calculating data using file.py algorithm"""

        if not self.json_data:
            confirmed = messagebox.showwarning("No Data", " No Json Data to calculate!")

        # Clears fields when making a new calculation
        self.grand_total_entry.delete(0, tk.END)
        self.cost_system_entry.delete(0, tk.END)
        self.tsc_cocomo_entry.delete(0, tk.END)
        self.atsc_entry.delete(0, tk.END)

        # Clears data dict in calculator.py
        self.estimator.clear()
        self.estimator.read_json_data(self.json_data)

        # gets calculation methods from calculator
        grand_total = self.estimator.total_system_cost()
        system_cost = self.estimator.cost_per_system()
        cocomo_cost = self.estimator.cocomo_estimation("Organic")
        actual_staff_cost = self.estimator.total_staff_cost()
        self.grand_total_entry.insert(0, grand_total)
        self.cost_system_entry.insert(0, system_cost)
        self.tsc_cocomo_entry.insert(0, cocomo_cost)
        self.atsc_entry.insert(0, actual_staff_cost)


start = GuiMain()
start.open_app()
