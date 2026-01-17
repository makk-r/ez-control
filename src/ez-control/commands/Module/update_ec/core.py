
import requests
import json
from packaging import version
from colorama import Fore, Style

def check_update(type_install, version_now, update):
    new_version_web = requests.get("https://raw.githubusercontent.com/makk-r/ez-control/refs/heads/main/public/web/pull_version.json")
    if new_version_web.status_code == 200:
        new_version_json = new_version_web.json()
        try:
            version_new = version.parse(new_version_json[type_install][update])
            version_now = version.parse(version_now)
            if version_new > version_now:
                return True
            else:
                return False
        except KeyError:
            print(f"{Fore.YELLOW}The system doesn't know how to install it.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Unable to connect.{Style.RESET_ALL}")
    return False
