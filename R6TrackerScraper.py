import requests
import bs4 as bs
from Manage_json import decode_json, save_json, get_profiles


url = "https://r6.tracker.network/profile/pc/"


def update_all_profile_levels():
    files = get_profiles()
    for file in files:
        data = decode_json(file)
        num_accounts = data["Accounts"]
        for y in range(num_accounts):
            key = "Player" + str(y+1)
            name = data[key]["Name"]
            account_url = url + name
            account_html = requests.get(account_url)
            if account_html.status_code == 200:
                soup = bs.BeautifulSoup(account_html.content, "lxml")
                get_level = soup.find(class_="trn-defstat__value")
                level = int(get_level.string)
                print(f"{name} -> {level}")
                data[key]["Level"] = level
            else:
                print(f"update_all_profile_levels() -> Account in {file} does not exist! -> {name}"
                      f"\nCheck if account name is up to date!")
                continue
        save_json(data["Owner"], data)


def update_profile_levels(profile_name):
    data = decode_json(profile_name + ".json")
    num_accounts = data["Accounts"]
    for x in range(num_accounts):
        key = "Player" + str(x+1)
        name = data[key]["Name"]
        account_url = url + name
        account_html = requests.get(account_url)
        if account_html.status_code == 200:
            soup = bs.BeautifulSoup(account_html.content, "lxml")
            get_level = soup.find(class_="trn-defstat__value")
            level = int(get_level.string)
            print(f"{name} -> {level}")
            data[key]["Level"] = level
        else:
            print(f"update_profile_levels({profile_name}) -> {name} does not exist!"
                  f"\nCheck if account name is up to date!")
        continue
    save_json(data["Owner"], data)


def get_account_level(account_name):
    account_url = url + account_name
    account_html = requests.get(account_url)
    if account_html.status_code == 200:
        soup = bs.BeautifulSoup(account_html.content, "lxml")
        get_level = soup.find(class_="trn-defstat__value")
        level = int(get_level.string)
        print(f"{account_name} -> {level}")
        return level
    else:
        print(f"get_account_level{account_name} -> Account does not exist!"
              f"\nCheck if account name is up to date!")
        return



    