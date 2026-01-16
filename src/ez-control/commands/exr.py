from colorama import Fore, Style
from .Module import github_ec, project
import os
import json
import shutil

file_path = os.path.abspath(__file__)

dir_path = os.path.dirname(file_path)

def load_program():
    with open(f"{dir_path}/program.json") as f:
        return json.load(f)

def check():
    data_app = load_program()
    len_project = project.len_project()
    print(f"name : {Fore.BLUE}{data_app["name"]}{Style.RESET_ALL}")
    print(f"version : {Fore.BLUE}{data_app["version"]}{Style.RESET_ALL}")
    print(f"\ncommand : {Fore.GREEN}online{Style.RESET_ALL}")
    print(f"project : {Fore.GREEN}{len_project}{Style.RESET_ALL}")

def git_ce(comm):
    comm = comm.split(" ")
    if len(comm) == 4:
        if comm[1] == "acc":
            if comm[2] == "set":
                github_ec.set_token(comm[3])
        elif comm[1] == "conn":
            github_ec.connect_project(comm[2], comm[3])

    if len(comm) == 3:
        if comm[1] == "acc":
            if comm[2] == "get":
                github_ec.get_acc()
            elif comm[2] == "out":
                github_ec.log_out_acc()

def command_project(comm):
    comm = comm.split(" ")
    if len(comm) == 3:
        if comm[1] == "build":
            project.build_project(comm[2])
        if comm[1] == "search":
            project.search_project(comm[2])
        if comm[1] == "open":
            project.correct_project(comm[2])
        if comm[1] == "lock":
            project.lock_project(comm[2])
        if comm[1] == "delete":
            project.delete_project(comm[2])
    elif len(comm) == 4:
        if comm[1] == "clone":
            project.cloning(comm)
    elif len(comm) == 2:
        if comm[1] == "show":
            project.see_project()
    else:
        print(
            """
All commands
Project editing
    pj build <name>                 : Create a project
    pj open <name>                  : Open VS Code on your project.
    pj delete <name>                : Delete project
    pj lock <name>                  : Lock project
    pj clone <path your_pc> <name>  : Create a project that already contains a folder.
Search
    pj search <name>                : Search for project
    pj show                         : Show all projects
            """
        )
