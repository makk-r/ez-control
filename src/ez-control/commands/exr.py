from colorama import Fore, Style

from .Module import app, github, project

def check():
    data_app = app.__data__
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
                acc = comm[3]
                github.set_acc(acc)
    if len(comm) == 3:
        if comm[1] == "acc":
            if comm[2] == "see":
                github.see_acc()

def command_project(comm):
    comm = comm.split(" ")
    if len(comm) == 3:
        if comm[1] == "b":
            project.build_project(comm[2])
        if comm[1] == "s":
            project.search_project(comm[2])
        if comm[1] == "c":
            project.correct_project(comm[2])
        if comm[1] == "lock":
            project.lock_project(comm[2])
        if comm[1] == "d":
            project.delete_project(comm[2])
        
    if len(comm) == 2:
        if comm[1] == "l":
            project.see_project()