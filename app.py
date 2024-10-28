import os
from colorama import init, Fore 
from utils import print_options, validate_user_input
from functions import create_new_file, print_files, add_data, get_data
import json

# Initialize colorama
init(autoreset=True)

config_file_path = os.path.join(os.getcwd(), ".config")
with open(config_file_path, "r") as file:
    json_data = json.load(file)


def main():
    storage_path = json_data.get("storage_path")

    if storage_path and not os.path.exists(storage_path):
        os.mkdir(storage_path)

    while True:
        print_options()
        user_input = input(Fore.LIGHTYELLOW_EX + "Select from above: ")
        validate_user_input(user_input)

        number = int(user_input)

        if number == 1: create_new_file()
        elif number == 2: print_files()
        elif number == 3: add_data()
        elif number == 4: get_data()
        elif number == 5: return

if __name__ == "__main__":
    main()
