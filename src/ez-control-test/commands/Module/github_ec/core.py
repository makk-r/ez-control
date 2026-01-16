
from colorama import Fore, Style
import json
import os
from datetime import datetime
from github import Github, GithubException
import sys

file_path = os.path.abspath(__file__)

dir_path = os.path.dirname(file_path)

def acc_check():
    if os.path.isfile(f"{dir_path}/data.json"):
        with open(f"{dir_path}/data.json", mode="r") as f:
            try:
                data_user_file = json.load(f)
                g = Github(data_user_file["token"])
                user = g.get_user()
                user_login = user.login
                return user
            except GithubException as e:
                return False
            except json.JSONDecodeError as e:
                return False

def get_acc():
    acc = ""
    try:
        with open(f"{dir_path}/data.json", mode="r") as f:
            data = json.load(f)
        acc = data["user"]
    except Exception:
        print(f"{Fore.YELLOW}error{Style.RESET_ALL}")
    print(f"account : {Fore.GREEN}{acc}{Style.RESET_ALL}")
    print("status : ", end="")
    if acc_check():
        print(f"{Fore.GREEN}online{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Offline{Style.RESET_ALL}")

def set_token(token):
    try:
        g = Github(token)
        user = g.get_user()
        status_login = user.login
    except GithubException as e:
        print(e)
        if e.status == 401:
            print(f"set account : {Fore.RED}token_error{Style.RESET_ALL}")
            return False
    data = {
        "user" : user.login,
        "name" : user.name,
        "token" : token
    }
    with open(f"{dir_path}/data.json", mode="w") as f:
        json.dump(data, f)
    print(f"set account : {Fore.GREEN}succeed{Style.RESET_ALL}")
    sys.exit(0)

def log_out_acc():
    if os.path.isfile(f"{dir_path}/data.json"):
        os.remove(f"{dir_path}/data.json")
        print(f"{Fore.GREEN}Logged out of account successfully.{Style.RESET_ALL}")
        sys.exit(0)
    else:
        print(f"{Fore.YELLOW}No Account{Style.RESET_ALL}")

