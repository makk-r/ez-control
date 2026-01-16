
import os
from colorama import Fore, Style
from datetime import datetime
import pandas as pd
import json
import shutil

file_path = os.path.abspath(__file__)

dir_path = os.path.dirname(file_path)

def check_lock(name):
    with open(f"{dir_path}/data/{name}/setup.json", mode="r") as f:
        set_up = json.load(f)
    return set_up["lock"]
    

if not os.path.isdir(f"{dir_path}/data/"):
    os.mkdir(f"{dir_path}/data/")

def lock_project(name):
    if os.path.isdir(f"{dir_path}/data/{name}"):
        with open(f"{dir_path}/data/{name}/setup.json", mode="r") as f:
            set_up = json.load(f)
        set_up["lock"] = True
        with open(f"{dir_path}/data/{name}/setup.json", mode="w") as f:
            json.dump(set_up, f)
    else:
        print(f"{Fore.YELLOW}No projects.{Style.RESET_ALL}")

def correct_project(name):
    if os.path.isdir(f"{dir_path}/data/{name}"):
        if check_lock(name):
            print(f"{Fore.YELLOW}The project has been locked.{Style.RESET_ALL}")
            return False
        try:
            os.system(f"code {dir_path}/data/{name}/main")
        except SystemError:
            print(f"{Fore.RED}There is no Visual Studio Code.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}No projects.{Style.RESET_ALL}")

def see_project():
    pjs = os.listdir(f"{dir_path}/data/")
    data_setup = {}
    for it in pjs:
        with open(f"{dir_path}/data/{it}/setup.json", mode="r") as f:
            data_setup[it] = json.load(f)
    ts = []
    ls =  []
    for id, it in data_setup.items():
        ts.append(it["time"])
        ls.append(it["lock"])
    
    data = {
        "name" : pjs,
        "lock" : ls,
        "time" : ts,
    }
    df = pd.DataFrame(data)
    print(df)

def search_project(name):
    pjs = os.listdir(f"{dir_path}/data/")
    data_setup = {}
    for it in pjs:
        with open(f"{dir_path}/data/{it}/setup.json", mode="r") as f:
            data_setup[it] = json.load(f)
    ts = []
    ls =  []
    for id, it in data_setup.items():
        ts.append(it["time"])
        ls.append(it["lock"])
    
    data = {
        "name" : pjs,
        "lock" : ls,
        "time" : ts,
    }
    df = pd.DataFrame(data)
    result = df[df['name'].str.contains(name)]
    print(result)

def build_project(name):
    if not os.path.isdir(f"{dir_path}/data/{name}"):
        os.mkdir(f"{dir_path}/data/{name}")
        os.mkdir(f"{dir_path}/data/{name}/main")
    else:
        print(f"{Fore.YELLOW}It already exists.{Style.RESET_ALL}")
        return False
    setting = {
        "lock" : False,
        "time" : datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    with open(f"{dir_path}/data/{name}/setup.json", mode="w") as f:
        json.dump(setting, f)
    return f"{dir_path}/data/{name}"

def delete_project(name):
    if os.path.isdir(f"{dir_path}/data/{name}"):
        if check_lock(name):
            print(f"{Fore.YELLOW}The project has been locked.{Style.RESET_ALL}")
            return False
        if input("Are you sure? [y/n]").upper() == "Y":
            shutil.rmtree(f"{dir_path}/data/{name}")
            print(f"{Fore.GREEN}Delete successful.{Style.RESET_ALL}")

def len_project():
    return len(os.listdir(f"{dir_path}/data/"))

def cloning(comm):
    if comm[3]:
        if not os.path.isdir(comm[3]):
            return False
    if comm[2]:
        path = build_project(comm[2])
        if not path:
            print(f"{Fore.YELLOW}Cancel. There was an error.{Style.RESET_ALL}")
    if comm[3]:
        shutil.copytree(comm[3], f"{path}/main/", dirs_exist_ok=True)