from colorama import Fore, Style
import os
from .exr import *

def run(command):
    if command == "ck":
        check()
        return True
    if command == "clear":
        os.system("clear")
        return True
    if command.startswith("git"):
        git_ce(command)
        return True
    if command.startswith("pj"):
        command_project(command)
        return True
    return False