"""required imports"""

import getpass
import json
import os
import re
import gnupg
from colorama import init, Fore, Style

init()

path = os.path.join(os.getcwd(), "../.gnupg")
data_path = os.path.join(os.getcwd(), ".pass_storage")
gpg = gnupg.GPG(gnupghome=path)
auth_data = {"current_passphrase": None, "current_file": None}


def create_new_file(file_name, passphrase):
    """A Function to create a new file to store the secrets"""

    while True:
        verify_passphrase = getpass.getpass("Enter a passphrase again: ")
        if passphrase == verify_passphrase:
            break

        print(Fore.LIGHTRED_EX + "Passphrase Didn't matched!")
        print(Style.RESET_ALL)

    file_path = os.path.join(data_path, f"{file_name}.json.gpg")
    gpg.encrypt(
        "[]",
        recipients=None,
        symmetric="AES256",
        passphrase=passphrase,
        output=file_path,
    )


def decrypt_json(encrypted_file, passphrase):
    """Function to decrypt the encrypted gpg file"""

    with open(encrypted_file, "rb") as file:
        decrypted_data = gpg.decrypt_file(file, passphrase=passphrase)

    if decrypted_data.ok:
        return json.loads(str(decrypted_data))

    print(Fore.LIGHTRED_EX + "Decryption failed!\n")
    print(Style.RESET_ALL)
    return None


def add_new_data(file_name, passphrase):
    """Function to add new data data to encrypted gpg file"""

    actual_file_path = os.path.join(data_path, f"{file_name}.json.gpg")
    if not os.path.exists(actual_file_path):
        print(Fore.LIGHTRED_EX + "File Does not exists!")
        return

    json_data = decrypt_json(actual_file_path, passphrase)
    if json_data is None:
        auth_data["current_file"] = None
        auth_data["current_passphrase"] = None
        return

    new_data = {}
    new_data["key"] = input(Fore.LIGHTYELLOW_EX + "Object_Key: ")
    print("")
    while True:
        key = input(Fore.BLUE + "key: ")
        if key == "exit":
            break

        value = input(Fore.CYAN + f"{key}: ")
        new_data[key] = value
        print("")

    json_data.append(new_data)

    gpg.encrypt(
        json.dumps(json_data, indent=4, separators=(",", ": ")),
        recipients=None,
        symmetric="AES256",
        passphrase=passphrase,
        output=actual_file_path,
    )
    print(Style.RESET_ALL)


def get_data(file_name, passphrase):
    """Function to retrieve the data from the encrypted file"""

    actual_file_path = os.path.join(data_path, f"{file_name}.json.gpg")
    if not os.path.exists(actual_file_path):
        print(Fore.LIGHTRED_EX + "File Does not exists!")
        return

    json_data = decrypt_json(actual_file_path, passphrase)
    if json_data is None:
        auth_data["current_file"] = None
        auth_data["current_passphrase"] = None
        return

    object_key = input(Fore.LIGHTYELLOW_EX + "Object_Key: ")
    regex = re.compile(object_key, re.IGNORECASE)
    result = [data for data in json_data if regex.search(data["key"])]
    print(Fore.LIGHTBLACK_EX + json.dumps(result, indent=4, separators=(",", ": ")))
    print(Style.RESET_ALL)


def print_options():
    """Print options on the command line"""

    print(Fore.LIGHTMAGENTA_EX + "1. Create new file")
    print("2. Add data")
    print("3. Get data")
    print("4. exit")
    print(Style.RESET_ALL)


def validate_user_input(user_input):
    """This function validates the user input"""

    while True:
        try:
            number = int(user_input)
            if number < 1 or number > 4:
                print(Fore.LIGHTRED_EX + "Please choose options from 1, 2, 3, or 4\n")
                user_input = input(Fore.LIGHTBLACK_EX + "Try Again: ")
            else:
                break
        except ValueError:
            print(Fore.LIGHTRED_EX + "Invalid input. Please enter a number.\n")
            user_input = input(Fore.LIGHTBLACK_EX + "Try Again: ")


def main():
    """The execution starts from here"""

    if not os.path.exists(data_path):
        os.mkdir(data_path)

    while True:
        print_options()
        user_input = input("Select from above: ")
        validate_user_input(user_input)

        print(Style.RESET_ALL)
        number = int(user_input)

        if number == 1:
            new_file_name = input(Fore.LIGHTYELLOW_EX + "File_Name: ")
            new_passphrase = getpass.getpass(Fore.LIGHTBLACK_EX + "Passphrase: ")
            create_new_file(new_file_name, new_passphrase)
            auth_data["current_passphrase"] = None
            auth_data["current_file"] = None

        elif number == 2:
            if auth_data["current_file"] is None:
                auth_data["current_file"] = input(Fore.LIGHTYELLOW_EX + "File_Name: ")
            if auth_data["current_passphrase"] is None:
                auth_data["current_passphrase"] = getpass.getpass(
                    Fore.LIGHTBLACK_EX + "Passphrase: "
                )

            add_new_data(auth_data["current_file"], auth_data["current_passphrase"])

        elif number == 3:
            if auth_data["current_file"] is None:
                auth_data["current_file"] = input(Fore.LIGHTYELLOW_EX + "File_Name: ")
            if auth_data["current_passphrase"] is None:
                auth_data["current_passphrase"] = getpass.getpass(
                    Fore.LIGHTBLACK_EX + "Passphrase: "
                )

            get_data(auth_data["current_file"], auth_data["current_passphrase"])
            print()

        elif number == 4:
            return


main()
