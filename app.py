import os
from colorama import init, Fore
from utils import print_options, take_option_input, exitHandler, getConfigData
from functions import create_new_file, print_files, add_data, get_data, get_object_list

# Initialize colorama
init(autoreset=True)

# Get the configuration data
json_data = getConfigData()


def main():
    """Main function execution starts from here"""

    # If Storage path is not defined then create new one
    storage_path = json_data.get("storage_path")
    if storage_path is None:
        exitHandler("Storage path is not configured!")

    storage_path = os.path.expanduser(storage_path)
    if not os.path.exists(storage_path):
        os.mkdir(storage_path)

    while True:
        print_options()
        user_input = take_option_input()

        if user_input == "1":
            create_new_file()
        elif user_input == "2":
            get_object_list()
        elif user_input == "3":
            print_files()
        elif user_input == "4":
            add_data()
        elif user_input == "5":
            get_data()
        elif user_input == "6":
            os._exit(1)
        else:
            print(Fore.LIGHTRED_EX + "Please choose appropriate option!")


if __name__ == "__main__":
    main()
