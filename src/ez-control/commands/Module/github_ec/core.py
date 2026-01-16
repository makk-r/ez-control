
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

def connect_project(name_project,name_repo):
    global dir_path
    module_dir_path = os.path.dirname(dir_path)
    project_path = f"{module_dir_path}/project/data/{name_project}"
    print(project_path)
    if not acc_check():
        print(f"{Fore.YELLOW}Not logged in.{Style.RESET_ALL}")
        return False
    if os.path.isdir(project_path):
        with open(f"{dir_path}/data.json", mode="r") as f:
            data = json.load(f)
        g = Github(data["token"])
        github_folder_path = f"{data["user"]}/{name_repo}"
        repo = g.get_repo(github_folder_path)
        
        message = input("message : ")
        
        contents = repo.get_contents("", ref="main")

        try:
            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path, ref="main"))
                else:
                    repo.delete_file(
                        path=file_content.path,
                        message=f"clear",
                        sha=file_content.sha,
                        branch="main"
                    )
        except GithubException as e:
            print(f"{Fore.RED}error{Style.RESET_ALL} : ")
        
        for root, dirs, files in os.walk(project_path):
            for filename in files:
                local_path = os.path.join(root, filename)
                relative_path = os.path.relpath(local_path, project_path)
            
                with open(local_path, "rb") as f:
                    content = f.read()
                
                try:
                    repo.create_file(
                        path=relative_path.replace("\\", "/"),
                        message=message,
                        content=content,
                        branch="main"
                    )
                    print(f"{Fore.GREEN}Success{Style.RESET_ALL} : {relative_path}")
                except Exception as e:
                    print(f"{Fore.RED}Error uploading {relative_path}{Style.RESET_ALL} : {e}")
    else:
        print(f"{Fore.YELLOW}The repo or project is incorrect.{Style.RESET_ALL}")

