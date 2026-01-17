
from colorama import Fore, Style
import json
import os
from datetime import datetime
from github import Github, GithubException
import sys

file_path = os.path.abspath(__file__)

dir_path = os.path.dirname(file_path)

def github_pull():
    if os.path.isfile(f"{dir_path}/data.json"): 
        with open(f"{dir_path}/data.json", mode="r") as f:
            try:
                data_user_file = json.load(f)
                g = Github(data_user_file["token"])
                user = g.get_user()
                user_login = user.login
                return g
            except GithubException as e:
                return False
            except json.JSONDecodeError as e:
                return False

def acc_check():
    g = github_pull()
    if g:
        return g.get_user()
    else:
        return False

def repo_check():
    global dir_path
    module_dir_path = os.path.dirname(dir_path)
    pjs = f"{module_dir_path}/project/data"
    dirs = os.listdir(pjs)
    g = github_pull()
    if g:
        for dir in dirs:
            dir_pj = os.path.join(pjs, dir)
            setup_pj = os.path.join(dir_pj, "setup.json")
            error = False
            try:
                with open(setup_pj, mode="r") as f:
                    setup_pj_data = json.load(f)
            except json.JSONDecodeError:
                error = True
            except FileNotFoundError:
                error = True
            if error:
                print(f"{Fore.RED}Project damaged.{Style.RESET_ALL}")
                return False
            if setup_pj_data["repo"] and g:
                try:
                    repo = g.get_repo(setup_pj_data["repo"])
                    print(f"{repo.name} : {Fore.GREEN}good{Style.RESET_ALL}")
                except GithubException:
                    print(f"{dir} : {Fore.RED}bad{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}The check has been cancelled and cannot be linked to the account.{Style.RESET_ALL}")
            

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
    if not acc_check():
        print(f"{Fore.YELLOW}Not logged in.{Style.RESET_ALL}")
        return False
    if os.path.isdir(project_path):
        try:
            if os.path.isfile(f"{project_path}/setup.json"):
                with open(f"{project_path}/setup.json", mode="r") as f:
                    setup_pj = json.load(f)
            with open(f"{dir_path}/data.json", mode="r", encoding="utf-8") as f:
                data = json.load(f)
        except json.decoder.JSONDecodeError as e:
            print(f"{Fore.RED}Project damaged.{Style.RESET_ALL}")
            return False
            
        try:
            print(f"{Fore.YELLOW}Connecting...{Style.RESET_ALL}")
            g = Github(data["token"])
            repo = g.get_repo(name_repo)
            name_repo_ck = repo.name
            print(f"connect : {name_repo_ck} >> {Fore.GREEN}succeed{Style.RESET_ALL}")
        except GithubException:
            print(f"{Fore.YELLOW}Unable to connect.{Style.RESET_ALL}")
            return False
        
        setup_pj["repo"] = name_repo
        
        with open(f"{project_path}/setup.json", mode="w") as f:
            json.dump(setup_pj,f)
        
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
        print(f"{Fore.YELLOW}Project damaged.{Style.RESET_ALL}")

