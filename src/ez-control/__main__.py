
import socket
import os
import sys
import commands
from colorama import Fore, Style
from packaging import version
import platform
import time
import readline
from commands.Module import github_ec

name_user = socket.gethostname()
os_name = platform.system()

def pb(status):
    
    if isinstance(status, str):
        print(f"[ {Fore.YELLOW}{status}{Style.RESET_ALL} ]")
        return
    if status:
        print(f"[ {Fore.GREEN}{status}{Style.RESET_ALL} ]")
    else:
        print(f"[ {Fore.RED}{status}{Style.RESET_ALL} ]")

def check_start():
    version_python = version.parse(platform.python_version())
    print(f"version : ", end="")
    support_system = ["Linux"]
    
    Essential_Package = {
        'colorama' : False,
        'packaging' : False,
        'pandas' : False
    }
    
    status = {
        "version" : False,
        "os" : False
    }
    
    if version_python >= version.parse("3.14"):
        status["version"] = True
        print(f"{version_python} >= 3.14", end=" ")
        pb(status["version"])
    else:
        print(f"{version_python} >= 3.14")
        pb(status["version"])

    print("system : ", end="")
    
    if os_name in support_system:
        status["os"] = True
        print(f"{os_name}", end=" ")
        pb(status["os"])
    else:
        print(f"{os_name}", end=" ")
        pb(status["os"])
    
    print("account : ", end="")
    
    acc = github_ec.acc_check()
    
    if acc:
        global name_user
        name_user = acc.login
        print(f"{Fore.GREEN}{acc.login}{Style.RESET_ALL}", end=" ")
        pb(True)
    else:
        print(f"{Fore.YELLOW}No Account{Style.RESET_ALL}", end=" ")
        pb("SKIP")
    
    print("\n\nstatus")
    for id,it in status.items():
        print(f"{id} :", end=" ")
        pb(it)
        if it == False:
            return False
    return True

if not check_start():
    sys.exit(0)

time.sleep(3)

os.system("clear")

try:
    while True:
        comm = input(f"@{name_user}{Fore.GREEN}~>{Style.RESET_ALL}")
        succeed = commands.run(comm)
        if not succeed:
            print(f"{Fore.RED}What is < {comm} >{Style.RESET_ALL}")
except KeyboardInterrupt:
    print(f"\n\n\n{Fore.RED}stop{Style.RESET_ALL}")
    os.system("clear")

