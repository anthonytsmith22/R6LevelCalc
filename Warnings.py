from tkinter import messagebox


# If account name entry AND/OR account level entry or left unfilled
# A messagebox warning will display prompting the user to fill both fields
def add_account_warning_msg():
    print("\nDisplaying add_account_warning_msg")
    messagebox.showwarning("Account Addition Failure",
                           "Incomplete fields, have a name and level provided!")


# If adding profile there is no name entered in add_profile_entry
# Messagebox warning will display prompting user to fill add_profile_entry
def add_profile_no_profile_name_msg():
    print("\nDisplaying add_profile_no_profile_name_msg")
    messagebox.showwarning("Profile Creation Failure",
                           "No profile name specified!")


# If loading profile there is no name entered in load_profile_entry
# Messagebox warning will display prompting user to fill load_profile_entry
def load_profile_no_profile_name_msg():
    print("\nDisplaying load_profile_no_profile_name_msg")
    messagebox.showwarning("Profile Import Failure",
                           "No profile name specified!")


# If when attempting to load a profile and no file with name given is found
# Messagebox warning will display alerting user of no profile of given name
def load_profile_no_profile_found_msg():
    print("\nDisplaying load_profile_no_profile_found_msg")
    messagebox.showwarning("Profile Not Found",
                           "No profile with specified name exists.")


# In edit profile window if attempting to enter update for account that does not exist
# Messagebox warning will display alerting user there is no account to update
def load_update_account_invalid_account_update_msg():
    print("\nDisplaying load_update_account_invalid_account_update_msg")
    messagebox.showwarning("Invalid Account Update",
                           "Attempted to update account that does not exist.")
