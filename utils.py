import os
import re
import json
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)


def print_options():
    """Print options on the command line"""

    print(Fore.LIGHTYELLOW_EX + "1. Create new file")
    print(Fore.LIGHTYELLOW_EX + "2. List files")
    print(Fore.LIGHTYELLOW_EX + "3. Add data")
    print(Fore.LIGHTYELLOW_EX + "4. Get data")
    print(Fore.LIGHTYELLOW_EX + "5. Exit")


def exitHandler(message):
    """Prints the message and exits the program"""

    print(Fore.LIGHTRED_EX + message)
    os._exit(1)


def getConfigData():
    """Returns the configuration data form .config file"""

    config_file_path = os.path.join(os.getcwd(), ".config")

    # Check if file exists
    if not os.path.exists(config_file_path):
        exitHandler("Configuration file not found!")

    # Load the json data
    with open(config_file_path, "r") as file:
        json_data = json.load(file)

    return json_data


def take_option_input():
    """Takes input from the user for options and return the user input"""

    pattern = r"^[1-5]$"
    while True:
        user_input = input(Fore.CYAN + "Select from above: ")
        if re.match(pattern, user_input):
            break
        print(Fore.LIGHTRED_EX + "Invalid input! Please try again.")
    return user_input


def take_file_name():
    """Takes the file name input from the user and validates it and returns the taken filename"""

    pattern = r"^[a-zA-Z_][a-zA-Z0-9_]{2,}$"
    while True:
        file_name = input(Fore.LIGHTCYAN_EX + "File name: ")

        if re.match(pattern, file_name):
            break

        print(
            Fore.LIGHTRED_EX
            + "File name must be atleast 3 characters long and should contain only alphanumeric characters and underscore! Please try again"
        )

    return file_name


def check_if_aes_key_present(aes_key_path):
    """This function checks if the encryption key is present or not if not then exists the program"""

    if aes_key_path is None:
        print("encryption key path is not configured! Add key path in .config file")
        os._exit(1)
    if not os.path.exists(aes_key_path):
        print('encryption key not found! run "./gen-aes-key.sh" to generate the key.')
        os._exit(1)
    return
