
from colorama import Fore, Style
import json
import os
from datetime import datetime

file_path = os.path.abspath(__file__)

dir_path = os.path.dirname(file_path)

def set_acc(acc):
    data = {
        "user" : acc,
        "time" : datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    with open(f"{dir_path}/data.json", mode="w") as f:
        json.dump(data, f)
    print(f"set account : {Fore.GREEN}succeed{Style.RESET_ALL}")

def see_acc():
    acc = ""
    try:
        with open(f"{dir_path}/data.json", mode="r") as f:
            data = json.load(f)
        acc = data["user"]
    except Exception:
        print(f"{Fore.YELLOW}error{Style.RESET_ALL}")
    print(f"account : {Fore.GREEN}{acc}{Style.RESET_ALL}")