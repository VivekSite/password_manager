import os
import re
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def print_options():
    """Print options on the command line"""

    print(Fore.LIGHTMAGENTA_EX + "1. Create new file")
    print(Fore.LIGHTMAGENTA_EX + "2. List files")
    print(Fore.LIGHTMAGENTA_EX + "3. Add data")
    print(Fore.LIGHTMAGENTA_EX + "4. Get data")
    print(Fore.LIGHTMAGENTA_EX + "5. Exit")

def validate_user_input(user_input):
    """This function validates the user input"""

    while True:
        try:
            number = int(user_input)
            if number < 1 or number > 5:
                print(Fore.LIGHTRED_EX + "Please choose options from 1 to 5\n")
                user_input = input(Fore.LIGHTBLACK_EX + "Try Again: ")
            else:
                break
        except ValueError:
            print(Fore.LIGHTRED_EX + "Invalid input. Please enter a number.\n")
            user_input = input(Fore.LIGHTBLACK_EX + "Try Again: ")

def take_file_name():
    pattern = r"^[a-zA-Z_][a-zA-Z0-9_]{2,}$"
    while True:
        file_name = input(Fore.LIGHTYELLOW_EX + "File name: ")
        
        if re.match(pattern, file_name):
            break

        print(Fore.LIGHTRED_EX + "File name must be atleast 3 characters long and should contain only alphanumeric characters and underscore! Please try again")

    return file_name


