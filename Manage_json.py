import json
import os
from Calculation import *


profiles_dir_path = "C:/Users/Anthony/PycharmProjects/LevelCalc/profiles/"


# In the main R6Calc frame, entered accounts that have name and level values stored in
# Lists, used provided new profile name as file name, and use the lists to create a dictionary
# That is dumped into profile_name.json in the LevelCalc/Profiles directory
def create_json(account_names, account_levels, profile_name):
    file_name = profile_name + ".json"
    data = {}
    counter = 0
    data["Owner"] = profile_name
    for x in account_names:
        player_key = "Player" + str(counter+1)
        data[player_key] = {"Name": x,
                            "Level": account_levels[counter]}
        counter += 1
    data["Accounts"] = counter
    path_name = os.path.join(profiles_dir_path + file_name)
    with open(path_name, "w") as write_file:
        json.dump(data, write_file)
        write_file.close()
        print(f"create_json(account_names, account_levels, {profile_name}) -> File saved successfully")
    return


# Given a dictionary and file name, will save dictionary as a json as file_name.json
# In the LevelCalc/Profiles directory
def save_json(file_name, data):
    path_name = os.path.join(profiles_dir_path + file_name + ".json")
    with open(path_name, "w") as write_file:
        json.dump(data, write_file)
        write_file.close()
        print(f"save_json({path_name}, data) -> File saved successfully")
    return


# Given a file_name, file_name.json will be deleted from LevelCalc directory
def delete_json(file_name):
    path_name = os.path.join(profiles_dir_path + file_name + ".json")
    if os.path.isfile(path_name):
        os.remove(path_name)
        print(f"delete_file({path_name}) -> File deleted successfully!")
    else:
        print(f"delete_file({path_name}) -> Error -> File not found!")
    return


# Given a profile_name, profile_name.json from LevelCalc/Profiles directory will load given
# File into a dictionary for usage
# Else return -1 signaling that no such file exists
def decode_json(profile_name):
    path_name = os.path.join(profiles_dir_path + profile_name)
    if os.path.isfile(path_name):
        with open(path_name, "r") as read_file:
            data = json.load(read_file)
            read_file.close()
            print(f"decode_json({path_name}) -> File Found! -> File loaded to dictionary")
        return data
    else:
        print(f"decode_file({path_name}) -> File not found!")
        return -1


# Given file_name, file_name.json will be loaded into a dictionary and given account_name will be searched for
# If account with given account_name is found, account level will be changed to given level
def update_level_from_json(account_name, level, file_name):
    found_account = 0
    path_name = os.path.join(profiles_dir_path + file_name + ".json")
    if os.path.isfile(path_name):
        print(f"update_level_from_json({account_name}, {level}, {file_name}) -> File found!")
        with open(path_name, "r") as read_file:
            data = json.load(read_file)
            read_file.close()
        num_accounts = data["Accounts"]
        for x in range(num_accounts):
            player_key = "Player" + str(x + 1)
            if data[player_key]["Name"] == account_name:
                found_account = 1
                data[player_key]["Level"] = level
                print(
                    f"update_level_from_json({account_name}, {level}, {file_name}) -> Account found -> Level updated!")
                with open(path_name, "w") as write_file:
                    json.dump(data, write_file)
                    write_file.close()
                    print(f"update_level_from_json({account_name}, {level}, {file_name}) -> File saved!")
                return
        if found_account == 0:
            print(f"update_level_from_json({account_name}, {level}, {file_name}) -> No account by that name found!")
            return
    else:
        print(f"update_level_from_json({account_name}, {level}, {file_name}) -> Account not found! -> No changes made!")
        return -1


# Given file_name, file_name.json will be loaded into a dictionary and a given account_name will be searched for
# If account with given account_name is found, change account_name to new_account_name
def update_name_from_json(account_name, new_account_name, file_name):
    path_name = os.path.join(profiles_dir_path + file_name + ".json")
    found_account = 0
    if os.path.isfile(path_name):
        with open(path_name, "r") as read_file:
            data = json.load(read_file)
            read_file.close()
            print(f"update_name_from_json({account_name}, {new_account_name}, {file_name}) -> File found!")
        num_accounts = data["Accounts"]
        for x in range(num_accounts):
            player_key = "Player" + str(x + 1)
            if data[player_key]["Name"] == account_name:
                found_account = 1
                data[player_key]["Name"] = new_account_name
                print(f"update_name_from_json({account_name}, {new_account_name}, {file_name}) "
                      f"-> Account found -> Name updated!")
                with open(path_name, "w") as write_file:
                    json.dump(data, write_file)
                    write_file.close()
                    print(f"update_level_from_json({account_name}, {new_account_name}, {file_name}) -> File saved!")
                return
        if account_name == 0:
            print(f"update_name_from_json({account_name}, {new_account_name}, {file_name}) "
                  f"-> Account not found! -> No changes made!")
            return
    else:
        print(f"update_name_from_json({account_name}, {new_account_name}, {file_name}) "
              f"-> File not found! -> No changes made!")
        return -1


# Given file_name, file_name.json will be loaded into a dictionary and a given account_name will be searched for
# If account with given account_name is found, data[player_key]["Name"] == account_name will be deleted
# Then dictionary will be restructured to modify player_keys
# If data["Player1"] is deleted, then data["Player2"] through data["Player(N)"] will be shifted to
# data["Player1"] through data["Player(N-1)"], N being original number of accounts in dictionary
# Finally data["Accounts"] will become data["Accounts"] -= 1 to represent new number of accounts in profile
# data will be dumped back into json
def remove_account_from_json(account_name, file_name):
    path_name = os.path.join(profiles_dir_path + file_name + ".json")
    found_account = 0
    if os.path.isfile(path_name):
        print(f"remove_account_from_json({account_name}, {path_name}) -> File found! -> Searching for account.")
        with open(path_name, "r") as read_file:
            data = json.load(read_file)
        num_accounts = data["Accounts"]
        for x in range(num_accounts):
            player_key = "Player" + str(x + 1)
            if data[player_key]["Name"] == account_name:
                found_account = 1
                print(f"remove_account_from_json({account_name}, {path_name}) -> Successfully found account!")
                temp_key = player_key
                del data[player_key]
                print(f"remove_account_from_json({account_name}, {path_name}) -> Account Successfully Deleted")
                data["Accounts"] -= 1
                remaining = num_accounts - (x + 1)
                for y in range(remaining):
                    player_key = "Player" + str(y + x + 2)
                    data[temp_key] = data[player_key]
                    temp_key = player_key
                    del data[player_key]
                with open(path_name, "w") as write_file:
                    json.dump(data, write_file)
                print(f"remove_account_from_json({account_name}, {path_name}) -> Profile saved!")
                return
        if found_account == 0:
            print(f"remove_account({account_name}, data) -> Account Not Found! -> No changed made.")
            return
    else:
        print(f"remove_account_from_json({account_name}, {path_name}) -> File not found! -> No changed made.")
        return -1


# Given file_name, file_name.json will be loaded into a dictionary, then a new key will be added
# data["Player(num_accounts+1)] = {"Name": account_name, "Level": level}
# data will be dumped back into file_name.json
def add_account_to_json(account_name, level, file_name):
    path_name = os.path.join(profiles_dir_path + file_name + ".json")
    if os.path.isfile(path_name):
        print(f"add_account_to_json({account_name}, {level}, {file_name}.json) -> File Found! -> Accessing File")
        path_name = os.path.join(profiles_dir_path + file_name + ".json")
        with open(path_name, "r") as read_file:
            data = json.load(read_file)
        read_file.close()
        num_accounts = data["Accounts"]
        data["Player" + str(num_accounts + 1)] = {"Name": account_name,
                                                  "Level": level}
        data["Accounts"] = num_accounts + 1
        with open(path_name, 'w') as write_file:
            json.dump(data, write_file)
        print(f"add_account_to_json({account_name}, {level}, {file_name}.json) -> Account added. -> File saved!")
    else:
        print(f"add_account_to_json({account_name}, {level}, {file_name}.json) -> File not found!")


# Will gather list of all files in LevelCalc/profiles directory amd return the list
def get_profiles():
    if os.path.lexists(profiles_dir_path):
        print(f"get_profiles() -> Directory Found -> Directory loaded to list")
        files = os.listdir(profiles_dir_path)
        return files
    print(f"get_profiles() -> Directory not found")
    return -1


# Will calculate profile overall level without the use of data and level lists utilized
# in the calculator tab, instead reading from the profile json
def calculate_level_from_json(profile_name):
    print("\ncalculate_level_from_json()")
    data = decode_json(profile_name + ".json")
    num_accounts = data["Accounts"]
    xp_total = 0
    for x in range(num_accounts):
        key = "Player" + str(x + 1)
        level = data[key]["Level"]
        xp_total += get_xp(int(level))
    total_level = get_level(xp_total)
    return total_level



