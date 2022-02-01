from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from Calculation import *
from Manage_json import *
from Warnings import *
from R6TrackerScraper import *


# Go to line 600
class R6Calc:

    # Holds account level and name values
    levels = []
    names = []

    # Clears all fields and lists in the main calculator window
    def clear_app(self):
        print("\nClearing main window")
        self.names.clear()
        self.levels.clear()
        self.account_name_entry.delete(0, END)
        self.account_level_entry.delete(0, END)
        self.lvl_entry.delete(0, END)
        self.add_profile_entry.delete(0, END)
        self.load_profile_entry.delete(0, END)
        self.add_account_description()

    # Bound to add_account_button, once button is hit, a check will run
    # to see if required entries have information entered
    # If one or more entries are empty, then a messagebox warning will be called
    # ELSE
    # Information from both entries will be retrieved, the level entry will be type casted
    # Information will be sent to corresponding lists, entries will be cleared
    # New information will be added to account_description label
    def add_account(self, event=None):
        print("\nadd_account()")
        self.lvl_entry.delete(0, END)
        if len(self.account_level_entry.get()) == 0 or len(self.account_name_entry.get()) == 0:
            add_account_warning_msg()
        else:
            account_level = self.account_level_entry.get()
            account_name = self.account_name_entry.get()
            self.levels.append(int(account_level))
            self.names.append(account_name)
            self.account_name_entry.delete(0, END)
            self.account_level_entry.delete(0, END)
            self.add_account_description()
        return

    def find_account(self, event=None):
        account_name = self.account_name_entry.get()
        level = get_account_level(account_name)
        self.account_level_entry.delete(0, END)
        self.account_level_entry.insert(0, level)

    # Bound to lvl_calculate_button, once hit will make use of methods from Calculation.py
    # to calculate the total level of all accounts
    # Level will be displayed to lvl_entry and remaining entries will be cleared
    # Lists will also be cleared for new calculation
    def calculate_level(self, event=None):
        print("\ncalculate_level()")
        xp_total = 0
        for x in self.levels:
            xp_total += get_xp(x)
        level = get_level(xp_total)
        self.lvl_entry.delete(0, END)
        self.lvl_entry.insert(0, level)
        self.account_level_entry.delete(0, END)
        self.levels.clear()
        self.names.clear()

    # Is called in add_account() method
    # Once information has been gathered, account name and level will be grabbed from lists
    # To create strVar() for accounts_label to display user with all accounts they have added
    def add_account_description(self):
        print("\nadd_account_description()")
        string = "Added Accounts\n************************************************\n"
        counter = 0
        for x in self.names:
            string += f"{x}\tLevel: {self.levels[counter]}\n"
            counter += 1
        self.account_text.set(string)
        return

    # Create new profile with provided name, all entered accounts will be saved to a json
    def add_profile(self, event=None):
        print("\nadd_profile()")
        if len(self.add_profile_entry.get()) == 0:
            add_profile_no_profile_name_msg()
        else:
            profile_name = self.add_profile_entry.get()
            file_name = profile_name
            print(f"add_profile(event=None) -> Create account -> Name[{profile_name}]")
            create_json(self.names, self.levels, file_name)
            print(f"add_profile(event=None) -> Profile created")
            self.add_profile_entry.delete(0, END)
            self.clear_app()

    # Will load profile and accounts based on entered profile name
    def load_profile(self, event=None):
        print("\nload_profile()")
        self.names.clear()
        self.levels.clear()
        if len(self.load_profile_entry.get()) == 0:
            load_profile_no_profile_name_msg()
        file_name = self.load_profile_entry.get()
        path_name = file_name + ".json"
        if decode_json(path_name) == -1:
            load_profile_no_profile_found_msg()
        else:
            print(f"decode_file({path_name}) -> File found -> Loading .json to dictionary")
            data = decode_json(path_name)
            num_accounts = data["Accounts"]
            for x in range(num_accounts):
                player_key = "Player" + str(x + 1)
                self.names.append(data[player_key]["Name"])
                self.levels.append(int(data[player_key]["Level"]))
        self.add_account_description()

    account_names = []

    # once profile to edit is selected in edit_profile_frame, will access all accounts
    # to edit
    def edit_profile_gather_accounts(self, event=None):
        print("\nedit_profile_gather_accounts()")
        self.clear_edit_list()
        self.account_names.clear()
        try:
            selected_profile = self.edit_profile_listbox.get(self.edit_profile_listbox.curselection())
            self.selected_profile_holder.set(selected_profile)
            file_name = selected_profile + ".json"
        except TclError:
            selected_profile = self.selected_profile_holder
            file_name = selected_profile.get() + ".json"
        profile_holder = decode_json(file_name)

        if "Player1" in profile_holder:
            self.edit_account_name_entry1.insert(0, profile_holder["Player1"]["Name"])
            self.edit_account_level_entry1.insert(0, profile_holder["Player1"]["Level"])
            self.account_names.append(profile_holder["Player1"]["Name"])
            self.edit_button_name1.set("Update Account")
            self.update_profile_button1.bind("<Button-1>", self.update_account1)
            self.remove_account_button1.bind("<Button-1>", self.remove_account1)
            self.remove_account_button1.grid(row=0, column=5, sticky=E, padx=2, pady=3)
        else:
            self.edit_button_name1.set("Add Account")
            self.remove_account_button1.grid_forget()
            self.update_profile_button1.bind("<Button-1>", self.add_account1)
        if "Player2" in profile_holder:
            self.edit_account_name_entry2.insert(0, profile_holder["Player2"]["Name"])
            self.edit_account_level_entry2.insert(0, profile_holder["Player2"]["Level"])
            self.account_names.append(profile_holder["Player2"]["Name"])
            self.edit_button_name2.set("Update Account")
            self.update_profile_button2.bind("<Button-1>", self.update_account2)
            self.remove_account_button2.bind("<Button-1>", self.remove_account2)
            self.remove_account_button2.grid(row=1, column=5, sticky=W, padx=2, pady=3)
        else:
            self.edit_button_name2.set("Add Account")
            self.remove_account_button2.grid_forget()
            self.update_profile_button2.bind("<Button-1>", self.add_account2)
        if "Player3" in profile_holder:
            self.edit_account_name_entry3.insert(0, profile_holder["Player3"]["Name"])
            self.edit_account_level_entry3.insert(0, profile_holder["Player3"]["Level"])
            self.account_names.append(profile_holder["Player3"]["Name"])
            self.edit_button_name3.set("Update Account")
            self.update_profile_button3.bind("<Button-1>", self.update_account3)
            self.remove_account_button3.bind("<Button-1>", self.remove_account3)
            self.remove_account_button3.grid(row=2, column=5, sticky=W, padx=2, pady=3)
        else:
            self.edit_button_name3.set("Add Account")
            self.remove_account_button3.grid_forget()
            self.update_profile_button3.bind("<Button-1>", self.add_account3)
        if "Player4" in profile_holder:
            self.edit_account_name_entry4.insert(0, profile_holder["Player4"]["Name"])
            self.edit_account_level_entry4.insert(0, profile_holder["Player4"]["Level"])
            self.account_names.append(profile_holder["Player4"]["Name"])
            self.edit_button_name4.set("Update Account")
            self.update_profile_button4.bind("<Button-1>", self.update_account4)
            self.remove_account_button4.bind("<Button-1>", self.remove_account4)
            self.remove_account_button4.grid(row=3, column=5, sticky=W, padx=2, pady=3)
        else:
            self.edit_button_name4.set("Add Account")
            self.remove_account_button4.grid_forget()
            self.update_profile_button4.bind("<Button-1>", self.add_account4)
        if "Player5" in profile_holder:
            self.edit_account_name_entry5.insert(0, profile_holder["Player5"]["Name"])
            self.edit_account_level_entry5.insert(0, profile_holder["Player5"]["Level"])
            self.account_names.append(profile_holder["Player5"]["Name"])
            self.edit_button_name5.set("Update Account")
            self.update_profile_button5.bind("<Button-1>", self.update_account5)
            self.remove_account_button5.bind("<Button-1>", self.remove_account5)
            self.remove_account_button5.grid(row=4, column=5, sticky=W, padx=2, pady=3)
        else:
            self.edit_button_name5.set("Add Account")
            self.remove_account_button5.grid_forget()
            self.update_profile_button5.bind("<Button-1>", self.add_account5)

    # Clears all entries in edit profile tab
    def clear_edit_list(self, event=None):
        print("\nclear_edit_list()")
        self.edit_account_name_entry1.delete(0, END)
        self.edit_account_level_entry1.delete(0, END)
        self.edit_account_name_entry2.delete(0, END)
        self.edit_account_level_entry2.delete(0, END)
        self.edit_account_name_entry3.delete(0, END)
        self.edit_account_level_entry3.delete(0, END)
        self.edit_account_name_entry4.delete(0, END)
        self.edit_account_level_entry4.delete(0, END)
        self.edit_account_name_entry5.delete(0, END)
        self.edit_account_level_entry5.delete(0, END)

    # Updates first account of a given profile in the edit profile tab
    def update_account1(self, event=None):
        print("\nupdate_account1()")
        orig_name = self.account_names[0]
        selected_profile = self.selected_profile_holder.get()
        new_name = self.edit_account_name_entry1.get()
        new_level = self.edit_account_level_entry1.get()
        update_level_from_json(orig_name, new_level, selected_profile)
        update_name_from_json(orig_name, new_name, selected_profile)

    # Updates second account of a given profile in the edit profile tab if present
    def update_account2(self, event=None):
        print("\nupdate_account2()")
        orig_name = self.account_names[1]
        selected_profile = self.selected_profile_holder.get()
        new_name = self.edit_account_name_entry2.get()
        new_level = self.edit_account_level_entry2.get()
        update_level_from_json(orig_name, new_level, selected_profile)
        update_name_from_json(orig_name, new_name, selected_profile)

    # Updates third account of a given profile in the edit profile tab if present
    def update_account3(self, event=None):
        print("\nupdate_account3()")
        orig_name = self.account_names[2]
        selected_profile = self.selected_profile_holder.get()
        new_name = self.edit_account_name_entry3.get()
        new_level = self.edit_account_level_entry3.get()
        update_level_from_json(orig_name, new_level, selected_profile)
        update_name_from_json(orig_name, new_name, selected_profile)

    # Updates fourth account of a given profile in the edit profile tab if present
    def update_account4(self, event=None):
        print("\nupdate_account4()")
        orig_name = self.account_names[3]
        selected_profile = self.selected_profile_holder.get()
        new_name = self.edit_account_name_entry4.get()
        new_level = self.edit_account_level_entry4.get()
        update_level_from_json(orig_name, new_level, selected_profile)
        update_name_from_json(orig_name, new_name, selected_profile)

    # Updates fifth account of a given profile in the edit profile tab if present
    def update_account5(self, event=None):
        print("\nupdate_account5")
        orig_name = self.account_names[4]
        selected_profile = self.selected_profile_holder.get()
        new_name = self.edit_account_name_entry5.get()
        new_level = self.edit_account_level_entry5.get()
        update_level_from_json(orig_name, new_level, selected_profile)
        update_name_from_json(orig_name, new_name, selected_profile)

    # Adds new account 1 to profile if none exists
    def add_account1(self, event=None):
        print("\nadd_account1()")
        selected_profile = self.selected_profile_holder.get()
        account_name = self.edit_account_name_entry1.get()
        account_level = self.edit_account_level_entry1.get()
        add_account_to_json(account_name, account_level, selected_profile)
        self.edit_button_name1.set("Update Profile")
        self.update_profile_button1.bind("<Button-1>", self.update_account1)
        self.remove_account_button1.bind("<Button-1>", self.remove_account1)
        self.remove_account_button1.grid(row=0, column=5, sticky=W, padx=2, pady=3)

    # Adds new account 2 to profile if none exists
    def add_account2(self, event=None):
        print("\nadd_account2()")
        selected_profile = self.selected_profile_holder.get()
        account_name = self.edit_account_name_entry2.get()
        account_level = self.edit_account_level_entry2.get()
        add_account_to_json(account_name, account_level, selected_profile)
        self.edit_button_name2.set("Update Profile")
        self.update_profile_button2.bind("<Button-1>", self.update_account2)
        self.remove_account_button2.bind("<Button-1>", self.remove_account2)
        self.remove_account_button2.grid(row=1, column=5, sticky=W, padx=2, pady=3)

    # Adds new account 3 to profile if none exists
    def add_account3(self, event=None):
        print("\nadd_account3()")
        selected_profile = self.selected_profile_holder.get()
        account_name = self.edit_account_name_entry3.get()
        account_level = self.edit_account_level_entry3.get()
        add_account_to_json(account_name, account_level, selected_profile)
        self.edit_button_name3.set("Update Profile")
        self.update_profile_button3.bind("<Button-1>", self.update_account3)
        self.remove_account_button3.bind("<Button-1>", self.remove_account3)
        self.remove_account_button3.grid(row=2, column=5, sticky=W, padx=2, pady=3)

    # Adds new account 4 to profile if none exists
    def add_account4(self, event=None):
        print("\nadd_account4()")
        selected_profile = self.selected_profile_holder.get()
        account_name = self.edit_account_name_entry4.get()
        account_level = self.edit_account_level_entry4.get()
        add_account_to_json(account_name, account_level, selected_profile)
        self.edit_button_name4.set("Update Profile")
        self.update_profile_button4.bind("<Button-1>", self.update_account4)
        self.remove_account_button4.bind("<Button-1>", self.remove_account4)
        self.remove_account_button4.grid(row=3, column=5, sticky=W, padx=2, pady=3)

    # Adds new account 5 to profile if none exists
    def add_account5(self, event=None):
        print("\nadd_account5()")
        selected_profile = self.selected_profile_holder.get()
        account_name = self.edit_account_name_entry5.get()
        account_level = self.edit_account_level_entry5.get()
        add_account_to_json(account_name, account_level, selected_profile)
        self.edit_button_name5.set("Update Profile")
        self.update_profile_button5.bind("<Button-1>", self.update_account5)
        self.remove_account_button5.bind("<Button-1>", self.remove_account5)
        self.remove_account_button5.grid(row=4, column=5, sticky=W, padx=2, pady=3)

    # Removes account 1 of profile
    def remove_account1(self, event=None):
        print("\nremove_account1()")
        account_name = self.edit_account_name_entry1.get()
        profile_name = self.selected_profile_holder.get()
        remove_account_from_json(account_name, profile_name)
        self.edit_account_name_entry1.delete(0, END)
        self.edit_account_level_entry1.delete(0, END)
        self.edit_button_name1.set("Add Account")
        self.update_profile_button1.bind("<Button-1>", self.add_account1)
        self.remove_account_button1.grid_forget()

    # Removes account 2 of profile
    def remove_account2(self, event=None):
        print("\nremove_account2()")
        account_name = self.edit_account_name_entry2.get()
        profile_name = self.selected_profile_holder.get()
        remove_account_from_json(account_name, profile_name)
        self.edit_account_name_entry2.delete(0, END)
        self.edit_account_level_entry2.delete(0, END)
        self.edit_button_name2.set("Add Account")
        self.update_profile_button2.bind("<Button-1>", self.add_account2)
        self.remove_account_button2.grid_forget()

    # Removes account 3 of profile
    def remove_account3(self, event=None):
        print("\nremove_account3()")
        account_name = self.edit_account_name_entry3.get()
        profile_name = self.selected_profile_holder.get()
        remove_account_from_json(account_name, profile_name)
        self.edit_account_name_entry3.delete(0, END)
        self.edit_account_level_entry3.delete(0, END)
        self.edit_button_name3.set("Add Account")
        self.update_profile_button3.bind("<Button-1>", self.add_account3)
        self.remove_account_button3.grid_forget()

    # Removes account 4 of profile
    def remove_account4(self, event=None):
        print("\nremove_account4()")
        account_name = self.edit_account_name_entry4.get()
        profile_name = self.selected_profile_holder.get()
        remove_account_from_json(account_name, profile_name)
        self.edit_account_name_entry4.delete(0, END)
        self.edit_account_level_entry4.delete(0, END)
        self.edit_button_name4.set("Add Account")
        self.update_profile_button4.bind("<Button-1>", self.add_account4)
        self.remove_account_button4.grid_forget()

    # Removes account 5 of profile
    def remove_account5(self, event=None):
        print("\nremove_account5()")
        account_name = self.edit_account_name_entry5.get()
        profile_name = self.selected_profile_holder.get()
        remove_account_from_json(account_name, profile_name)
        self.edit_account_name_entry5.delete(0, END)
        self.edit_account_level_entry5.delete(0, END)
        self.edit_button_name5.set("Add Account")
        self.update_profile_button5.bind("<Button-1>", self.add_account5)
        self.remove_account_button5.grid_forget()

    # Creates profile overview tab where all saved profiles are displayed with overall level
    # When GUI starts up, a list containing all profile json files that have been
    # loaded as dictionaries is created, use an enhanced for loop to iterate through
    # files, creating individual frames for each profile with profile name, account names,
    # Corresponding levels, and profile overall level
    def create_profile_overview_frame(self):
        print("\ncreate_profile_overview_frame()")
        profile_counter = 0

        for x in self.dict_files:
            profile_frame = Frame(self.compare_profile_frame)
            profile_name_frame = Frame(profile_frame)
            profile_account_names_frame = Frame(profile_frame)
            profile_account_levels_frame = Frame(profile_frame)
            profile_name = x["Owner"]
            num_accounts = x["Accounts"]
            profile_label = Label(profile_name_frame, text=profile_name)
            profile_label.grid(row=0, column=profile_counter, sticky=N, padx=5, pady=2)
            counter = 0
            for y in range(num_accounts):
                key = "Player" + str(counter + 1)
                name = x[key]["Name"]
                level = x[key]["Level"]
                account_name_label = Label(profile_account_names_frame, text=name)
                account_level_label = Label(profile_account_levels_frame, text="Level: " + str(level))
                account_name_label.grid(row=counter, column=0, sticky=NW, padx=2, pady=2)
                account_level_label.grid(row=counter, column=0, sticky=NE, padx=2, pady=2)
                counter += 1
            profile_level_label = Label(profile_account_names_frame, text="Total Level:")
            profile_level_label.grid(row=counter + 1, column=0, sticky=NW, padx=2, pady=2)
            profile_level_total_label = Label(profile_account_levels_frame,
                                              text=calculate_level_from_json(profile_name))
            profile_level_total_label.grid(row=counter + 1, column=0, sticky=NE, padx=2, pady=2)
            profile_name_frame.grid(row=0, column=0, sticky=NW, padx=5, pady=5)
            profile_account_names_frame.grid(row=1, column=0, sticky=NW, padx=5)
            profile_account_levels_frame.grid(row=1, column=1, sticky=NE)
            profile_frame.grid(row=0, column=profile_counter, sticky=N, padx=5, pady=5)
            profile_counter += 1
        self.compare_profile_frame.grid(row=0, column=0, sticky=N)

    # Retrieves selected profile from delete_profile_listbox and inserts it into delete_profile_entry
    def select_profile(self, event=None):
        select_profile = self.delete_profile_listbox.get(self.delete_profile_listbox.curselection())
        self.delete_profile_entry.delete(0, END)
        self.delete_profile_entry.insert(0, select_profile)

    # Deletes selected profile while saving json to dictionary for immediate recovery
    def delete_profile(self, event=None):
        print("\ndelete_profile()")
        selected_profile = self.delete_profile_entry.get()
        self.undo_delete_data.clear()
        self.undo_delete_data.append(decode_json(os.path.join(selected_profile + ".json")))
        delete_json(selected_profile)
        self.delete_profile_entry.delete(0, END)
        self.undo_delete_button.grid(row=0, column=3, sticky=NW, padx=0, pady=20)
        self.create_delete_listbox()

    # Undoes most recent profile deletion
    def undo_delete_profile(self, event=None):
        print("\nundo_delete_profile")
        data = self.undo_delete_data[0]
        save_json(data["Owner"], data)
        self.undo_delete_button.grid_forget()
        self.create_delete_listbox()

    # Goes through all profiles and their accounts to validate levels from r6.tracker.network
    def validate_levels(self, event=None):
        update_all_profile_levels()
        self.edit_profile_gather_accounts()

    # Goes through selected profile in edit_profile_frame and validates all account levels from
    # r6.tracker.network
    def validate_profile(self, event=None):
        profile_name = self.selected_profile_holder.get()
        update_profile_levels(profile_name)
        self.edit_profile_gather_accounts()

    # sets R6Calc frame to edit_profile_frame
    def load_edit_profile_frame(self, event=None):
        print("\nload_edit_profile_frame()")
        self.main_frame.grid_forget()
        self.compare_profile_frame.grid_forget()
        self.delete_profile_main_frame.grid_forget()
        self.create_edit_listbox()
        self.edit_profile_frame.grid(row=0, column=0, sticky=N)
        root.geometry("650x200+400+400")

    # Refresh edit_list_listbox with contents of profiles folder
    def create_edit_listbox(self):
        self.edit_profile_listbox.delete(0, END)
        self.load_all_profiles()
        counter = 1
        for z in self.profile_names:
            self.edit_profile_listbox.insert(counter, z)
            counter += 1

    # Refresh delete_profile_listbox with contents of profiles folder
    def create_delete_listbox(self):
        self.delete_profile_listbox.delete(0, END)
        self.load_all_profiles()
        counter = 1
        for i in self.profile_names:
            self.delete_profile_listbox.insert(counter, i)
            counter += 1

    # sets R6Calc frame to main_frame
    def load_main_frame(self, event=None):
        print("\nload_main_frame")
        self.edit_profile_frame.grid_forget()
        self.compare_profile_frame.grid_forget()
        self.delete_profile_main_frame.grid_forget()
        self.main_frame.grid(row=0, column=0, sticky=N)
        root.geometry("650x200+400+400")

    # Sets R6Calc frame to compare profile frame from create_profile_overview_frame()
    def load_compare_profile_frame(self, event=None):
        print("\nload_compare_profile_frame()")
        self.main_frame.grid_forget()
        self.edit_profile_frame.grid_forget()
        self.create_profile_overview_frame()
        self.delete_profile_main_frame.grid_forget()
        root.geometry("1000x200+400+400")

    # Sets R6Calc frame to delete_profile_main_frame
    def load_delete_profile_frame(self, event=None):
        print("\nload_delete_profile_frame()")
        self.main_frame.grid_forget()
        self.edit_profile_frame.grid_forget()
        self.compare_profile_frame.grid_forget()
        self.create_delete_listbox()
        self.delete_profile_main_frame.grid(row=0, column=0, sticky=N, padx=10, pady=10)
        root.geometry("650x220+400+400")

    def load_all_profiles(self):
        self.files = get_profiles()
        self.dict_files = []
        self.profile_names = []

        for x in self.files:
            self.dict_files.append(decode_json(x))

        for y in self.dict_files:
            self.profile_names.append(y["Owner"])

    def __init__(self, root):
        # Our GUI

        root.geometry("650x200+400+400")
        root.title("R6Calc")
        root.resizable(width=False, height=False)

        ######################################################################################
        # Main frame, where the calculator is located and profiles can be created and loaded
        # To calculate overall level
        self.main_frame = Frame(root)

        self.left_panel = Frame(self.main_frame)
        self.left_panel.grid(row=0, column=0, sticky=NW, padx=10)

        self.right_panel = Frame(self.main_frame)
        self.right_panel.grid(row=0, column=1, sticky=NW)

        # Frame 1 for adding accounts
        self.frame1 = Frame(self.left_panel)
        self.frame1.grid(row=0, column=0, sticky=NW)

        # Label for account name entry
        self.nameLabel = Label(self.frame1, text="Account Name")
        self.nameLabel.grid(row=0, column=0, sticky=W, padx=2)

        # Entry or account name
        self.account_name_entry = Entry(self.frame1, width=15)
        self.account_name_entry.grid(row=0, column=1, sticky=W, padx=2)

        # Button to find account with web scraping
        self.find_account_button = Button(self.frame1, text="Find Account")
        self.find_account_button.bind("<Button-1>", self.find_account)
        self.find_account_button.grid(row=0, column=2, sticky=EW, padx=0)

        # Label for account level entry
        self.account_lvl_label = Label(self.frame1, text="Account Level")
        self.account_lvl_label.grid(row=1, column=0, sticky=W, padx=2, pady=5)

        # Entry for account level
        self.account_level_entry = Entry(self.frame1, width=5)
        self.account_level_entry.grid(row=1, column=1, sticky=W, padx=2, pady=5)

        # Processes account name and level entries
        self.add_account_button = Button(self.frame1, text="Add Account")
        self.add_account_button.bind("<Button-1>", self.add_account)
        self.add_account_button.grid(row=1, column=2, sticky=EW, padx=0)

        # Label for combined level entry
        self.lvl_label = Label(self.frame1, text="Combined Level:    ")
        self.lvl_label.grid(row=2, column=0, sticky=W, padx=0, pady=10)

        # Entry for combined level
        self.lvl_entry = Entry(self.frame1, width=5)
        self.lvl_entry.grid(row=2, column=1, sticky=W, padx=0, pady=10)

        # Button to calculate combined level
        self.lvl_calc_button = Button(self.frame1, text="Calculate")
        self.lvl_calc_button.bind("<Button-1>", self.calculate_level)
        self.lvl_calc_button.grid(row=2, column=2, sticky=EW, padx=0, pady=10)

        # Frame 2 for displaying added accounts
        self.frame2 = Frame(self.right_panel)
        self.frame2.grid(row=0, column=0, sticky=N, padx=40, pady=0)

        # Label to display account names and levels
        self.account_text = StringVar()
        self.account_text.set("Added Accounts\n************************************************\n")

        self.accounts_label = Label(self.frame2, textvariable=self.account_text)
        self.accounts_label.grid(row=0, column=0, sticky=N, padx=0)

        ######################################################################################
        # Using Listbox for added accounts representation prototype
        # added_accounts = Listbox(self.frame2, hieght=50, width=50, selectmode=SINGLE)
        ######################################################################################

        # Frame 3 for adding profiles
        self.frame3 = Frame(self.left_panel)
        self.frame3.grid(row=1, column=0, sticky=SW, pady=40)

        self.add_profile_label = Label(self.frame3, text="New Profile")
        self.add_profile_label.grid(row=0, column=0, sticky=S, padx=2)

        self.add_profile_entry = Entry(self.frame3, width=18)
        self.add_profile_entry.grid(row=0, column=1, sticky=S, padx=10)

        self.add_profile_button = Button(self.frame3, text="Add Profile")
        self.add_profile_button.bind("<Button-1>", self.add_profile)
        self.add_profile_button.grid(row=0, column=2, sticky=EW, padx=2)

        self.load_profile_label = Label(self.frame3, text="Old Profile")
        self.load_profile_label.grid(row=1, column=0, sticky=SW, padx=2, pady=5)

        self.load_profile_entry = Entry(self.frame3, width=18)
        self.load_profile_entry.grid(row=1, column=1, sticky=SW, padx=10, pady=5)

        self.load_profile_button = Button(self.frame3, text="Load Profile")
        self.load_profile_button.bind("<Button-1>", self.load_profile)
        self.load_profile_button.grid(row=1, column=2, stick=EW, padx=2, pady=5)

        self.main_frame.grid(row=0, column=0, sticky=N)

        ######################################################################################
        # Window to edit existing profile, updating levels, names, adding, removing accounts

        self.edit_profile_frame = Frame(root, height=200, width=200)

        self.edit_profile_frame_left_panel = Frame(self.edit_profile_frame)
        self.edit_profile_frame_center_panel = Frame(self.edit_profile_frame)
        self.edit_profile_frame_right_panel = Frame(self.edit_profile_frame)

        # grabs all files from profiles directory and adds them to files[]
        # files are loaded into dictionaries into dict_files[]
        # grab all profile files' owner name and add them to profile_names[]
        self.files = get_profiles()
        self.dict_files = []
        self.profile_names = []

        # create listbox that uses profile names as options
        self.edit_profile_listbox = Listbox(self.edit_profile_frame_left_panel, selectmode=SINGLE)
        self.edit_profile_listbox.grid(row=0, column=0, sticky=N, padx=5, pady=5)

        # Button to update account levels from R6Tracker
        self.update_levels_from_tracker = Button(self.edit_profile_frame_left_panel, text="Validate Profiles")
        self.update_levels_from_tracker.bind("<Button-1>", self.validate_levels)
        self.update_levels_from_tracker.grid(row=1, column=0, sticky=E)

        # button to select profile from listbox
        self.edit_select_profile_button = Button(self.edit_profile_frame_center_panel, text="Select Profile")
        self.edit_select_profile_button.bind("<Button-1>", self.edit_profile_gather_accounts)
        self.edit_select_profile_button.grid(row=0, column=0, sticky=EW, pady=5)

        self.edit_clear_button = Button(self.edit_profile_frame_center_panel, text="Clear Selection")
        self.edit_clear_button.bind("<Button-1>", self.clear_edit_list)
        self.edit_clear_button.grid(row=1, column=0, sticky=EW, pady=10)

        self.validate_selected_profile_button = Button(self.edit_profile_frame_center_panel, text="Validate Profile")
        self.validate_selected_profile_button.bind("<Button-1>", self.validate_profile)
        self.validate_selected_profile_button.grid(row=2, column=0, sticky=EW, pady=5)

        # Holds name of selected profile from listbox
        self.selected_profile_holder = StringVar()

        # StringVars to update name of edit_buttons for either update profile or add profile
        self.edit_button_name1 = StringVar()
        self.edit_button_name1.set("Update Profile")

        self.edit_button_name2 = StringVar()
        self.edit_button_name2.set("Update Profile")

        self.edit_button_name3 = StringVar()
        self.edit_button_name3.set("Update Profile")

        self.edit_button_name4 = StringVar()
        self.edit_button_name4.set("Update Profile")

        self.edit_button_name5 = StringVar()
        self.edit_button_name5.set("Update Profile")

        # Profile 1 edit line
        self.name_label1 = Label(self.edit_profile_frame_right_panel, text="Account 1")
        self.edit_account_name_entry1 = Entry(self.edit_profile_frame_right_panel, width=16)
        self.level_label1 = Label(self.edit_profile_frame_right_panel, text="Level")
        self.edit_account_level_entry1 = Entry(self.edit_profile_frame_right_panel, width=3)
        self.update_profile_button1 = Button(self.edit_profile_frame_right_panel, textvariable=self.edit_button_name1)
        self.remove_account_button1 = Button(self.edit_profile_frame_right_panel, text="Remove")
        # update_profile_button1.bind("<Button-1>", update_profile)

        # Profile 2 edit line
        self.name_label2 = Label(self.edit_profile_frame_right_panel, text="Account 2")
        self.edit_account_name_entry2 = Entry(self.edit_profile_frame_right_panel, width=16)
        self.level_label2 = Label(self.edit_profile_frame_right_panel, text="Level")
        self.edit_account_level_entry2 = Entry(self.edit_profile_frame_right_panel, width=3)
        self.update_profile_button2 = Button(self.edit_profile_frame_right_panel, textvariable=self.edit_button_name2)
        self.remove_account_button2 = Button(self.edit_profile_frame_right_panel, text="Remove")
        # update_profile_button2.bind("<Button-1>", update_profile)

        # Profile 3 edit line
        self.name_label3 = Label(self.edit_profile_frame_right_panel, text="Account 3")
        self.edit_account_name_entry3 = Entry(self.edit_profile_frame_right_panel, width=16)
        self.level_label3 = Label(self.edit_profile_frame_right_panel, text="Level")
        self.edit_account_level_entry3 = Entry(self.edit_profile_frame_right_panel, width=3)
        self.update_profile_button3 = Button(self.edit_profile_frame_right_panel, textvariable=self.edit_button_name3)
        self.remove_account_button3 = Button(self.edit_profile_frame_right_panel, text="Remove")
        # update_profile_button3.bind("<Button-1>", update_profile)

        # Profile 4 edit line
        self.name_label4 = Label(self.edit_profile_frame_right_panel, text="Account 4")
        self.edit_account_name_entry4 = Entry(self.edit_profile_frame_right_panel, width=16)
        self.level_label4 = Label(self.edit_profile_frame_right_panel, text="Level")
        self.edit_account_level_entry4 = Entry(self.edit_profile_frame_right_panel, width=3)
        self.update_profile_button4 = Button(self.edit_profile_frame_right_panel, textvariable=self.edit_button_name4)
        self.remove_account_button4 = Button(self.edit_profile_frame_right_panel, text="Remove")
        # update_profile_button4.bind("<Button-1>", update_profile)

        # Profile 5 edit line
        self.name_label5 = Label(self.edit_profile_frame_right_panel, text="Account 5")
        self.edit_account_name_entry5 = Entry(self.edit_profile_frame_right_panel, width=16)
        self.level_label5 = Label(self.edit_profile_frame_right_panel, text="Level")
        self.edit_account_level_entry5 = Entry(self.edit_profile_frame_right_panel, width=3)
        self.update_profile_button5 = Button(self.edit_profile_frame_right_panel, textvariable=self.edit_button_name5)
        self.remove_account_button5 = Button(self.edit_profile_frame_right_panel, text="Remove")
        # update_profile_button5.bind("<Button-1>", update_profile)

        # profile 1 grid widgets to frame
        self.name_label1.grid(row=0, column=0, sticky=N, padx=2, pady=3)
        self.edit_account_name_entry1.grid(row=0, column=1, sticky=N, padx=2, pady=3)
        self.level_label1.grid(row=0, column=2, sticky=N, padx=2, pady=3)
        self.edit_account_level_entry1.grid(row=0, column=3, sticky=N, padx=2, pady=3)
        self.update_profile_button1.grid(row=0, column=4, sticky=EW, padx=2, pady=3)

        # profile 2 grid widgets to frame
        self.name_label2.grid(row=1, column=0, sticky=N, padx=2, pady=3)
        self.edit_account_name_entry2.grid(row=1, column=1, sticky=N, padx=2, pady=3)
        self.level_label2.grid(row=1, column=2, sticky=N, padx=2, pady=3)
        self.edit_account_level_entry2.grid(row=1, column=3, sticky=N, padx=2, pady=3)
        self.update_profile_button2.grid(row=1, column=4, sticky=EW, padx=2, pady=3)

        # profile 3 grid widgets to frame
        self.name_label3.grid(row=2, column=0, sticky=N, padx=2, pady=3)
        self.edit_account_name_entry3.grid(row=2, column=1, sticky=N, padx=2, pady=3)
        self.level_label3.grid(row=2, column=2, sticky=N, padx=2, pady=3)
        self.edit_account_level_entry3.grid(row=2, column=3, sticky=N, padx=2, pady=3)
        self.update_profile_button3.grid(row=2, column=4, sticky=EW, padx=2, pady=3)

        # profile 4 grid widgets to frame
        self.name_label4.grid(row=3, column=0, sticky=N, padx=2, pady=3)
        self.edit_account_name_entry4.grid(row=3, column=1, sticky=N, padx=2, pady=3)
        self.level_label4.grid(row=3, column=2, sticky=N, padx=2, pady=3)
        self.edit_account_level_entry4.grid(row=3, column=3, sticky=N, padx=2, pady=3)
        self.update_profile_button4.grid(row=3, column=4, sticky=EW, padx=2, pady=3)

        # profile 5 grid widgets to frame
        self.name_label5.grid(row=4, column=0, sticky=N, padx=2, pady=3)
        self.edit_account_name_entry5.grid(row=4, column=1, sticky=N, padx=2, pady=3)
        self.level_label5.grid(row=4, column=2, sticky=N, padx=2, pady=3)
        self.edit_account_level_entry5.grid(row=4, column=3, sticky=N, padx=2, pady=3)
        self.update_profile_button5.grid(row=4, column=4, sticky=EW, padx=2, pady=3)

        self.edit_profile_frame_left_panel.grid(row=0, column=0, sticky=N, padx=5, pady=5)
        self.edit_profile_frame_center_panel.grid(row=0, column=1, sticky=N, padx=5, pady=5)
        self.edit_profile_frame_right_panel.grid(row=0, column=2, sticky=N, padx=5, pady=5)

        ######################################################################################
        # Compare profiles frame
        self.compare_profile_frame = Frame(root)

        ######################################################################################
        # Delete Profiles frame
        self.undo_delete_data = []
        self.delete_profile_main_frame = Frame(root)
        self.delete_profile_listbox_frame = Frame(self.delete_profile_main_frame)
        self.delete_profile_listbox = Listbox(self.delete_profile_listbox_frame, selectmode=SINGLE)
        self.delete_profile_listbox.grid(row=0, column=0, sticky=N, padx=5, pady=5)
        self.delete_profile_select_button = Button(self.delete_profile_listbox_frame, text="Select Profile")
        self.delete_profile_select_button.grid(row=1, column=0, sticky=E, padx=5, pady=0)
        self.delete_profile_select_button.bind("<Button-1>", self.select_profile)
        self.delete_profile_frame = Frame(self.delete_profile_main_frame)
        self.delete_profile_label = Label(self.delete_profile_frame, text="Profile Name:")
        self.delete_profile_label.grid(row=0, column=0, sticky=NW, padx=10, pady=20)
        self.delete_profile_entry = Entry(self.delete_profile_frame, width=16)
        self.delete_profile_entry.grid(row=0, column=1, sticky=NW, padx=0, pady=20)
        self.delete_profile_button = Button(self.delete_profile_frame, text="Delete Profile")
        self.delete_profile_button.bind("<Button-1>", self.delete_profile)
        self.delete_profile_button.grid(row=0, column=2, sticky=NW, padx=10, pady=20)
        self.undo_delete_button = Button(self.delete_profile_frame, text="Undo")
        self.undo_delete_button.bind("<Button-1>", self.undo_delete_profile)
        self.delete_profile_listbox_frame.grid(row=0, column=0, sticky=N, padx=5, pady=5)
        self.delete_profile_frame.grid(row=0, column=1, sticky=N, padx=5, pady=5)

        # Menu bar
        # File menu bar
        self.the_menu = Menu(root)
        self.file_menu = Menu(self.the_menu, tearoff=0)

        self.file_menu.add_command(label="Open Profile")
        self.file_menu.add_command(label="New Profile", command=self.clear_app)
        self.file_menu.add_command(label="Save Profile", command=self.add_profile)
        self.file_menu.add_command(label="Edit Profile", command=self.load_edit_profile_frame)
        self.file_menu.add_command(label="Delete Profile", command=self.load_delete_profile_frame)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Return to Home", command=self.load_main_frame)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit Application", command=quit_app)

        # View menu
        self.view_menu = Menu(self.the_menu, tearoff=0)

        self.view_menu.add_command(label="Compare Profiles", command=self.load_compare_profile_frame)

        self.the_menu.add_cascade(label="File", menu=self.file_menu)
        self.the_menu.add_cascade(label="View", menu=self.view_menu)
        root.config(menu=self.the_menu)


# Closes root window
def quit_app():
    print("\nClosing R6Calculator")
    root.quit()
    print("R6Calculator closed successfully")


if __name__ == '__main__':
    root = Tk()
    calc = R6Calc(root)
    root.mainloop()
