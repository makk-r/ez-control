import socket
import os
import sys
import commands
from colorama import Fore, Style
from packaging import version
import platform
import time

name_user = socket.gethostname()
os_name = platform.system()

def pb(status):
    if status:
        print(f"[ {Fore.GREEN}{status}{Style.RESET_ALL} ]")
    else:
        print(f"[ {Fore.RED}{status}{Style.RESET_ALL} ]")

def check_start():
    version_python = version.parse(platform.python_version())
    print(f"version : ", end="")
    
    support_system = ["Linux"]
    
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
        return False
    if os_name in support_system:
        status["os"] = True
        print(f"system : {os_name}", end=" ")
        pb(status["os"])
    else:
        print(f"system : {os_name}", end=" ")
        pb(status["os"])
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

