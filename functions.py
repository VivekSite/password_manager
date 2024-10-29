import os
import re
import json
from colorama import init, Fore
from utils import take_file_name, check_if_aes_key_present, getConfigData, exitHandler
from decryption_util import decrypt_file, decrypt_key
from encryption_util import encrypt_file


# Initialize colorama
init(autoreset=True)

# Get the configuration data
json_data = getConfigData()

# Get the path of encryption key and storage
storage_path = json_data.get("storage_path")
aes_key_path = json_data.get("aes_key_path")

if storage_path is None:
    exitHandler("Storage path is not configured!")

if aes_key_path is None:
    exitHandler("Encryption key path is not configured!")

# redefine the variable with expanded path
storage_path = os.path.expanduser(storage_path)
aes_key_path = os.path.expanduser(aes_key_path)

# Perform necessary validations
if not os.path.exists(storage_path):
    os.mkdir(storage_path)

if not os.path.exists(aes_key_path):
    exitHandler(f"Encryption key not found! {aes_key_path}")

if os.path.exists(aes_key_path) and os.path.getsize(aes_key_path) == 0:
    exitHandler(f"Encryption key file is empty! {aes_key_path}")


def create_new_file():
    """Create a new Empty file"""

    # check if encryption key is present or not
    check_if_aes_key_present(aes_key_path)

    # take file name
    file_name = take_file_name()
    file_path = os.path.join(storage_path, f"{file_name}.json.enc")

    key = decrypt_key()  # decrypt the encryption key
    encrypt_file(file_path, json.dumps([]), key)  # encrypt the file

    print(Fore.LIGHTGREEN_EX + f"New file created successfully: {file_name}\n")


def print_files():
    """Prints all the available files"""

    filenames = [
        os.path.splitext(os.path.splitext(file)[0])[0]  # Remove the extension
        for file in os.listdir(storage_path)  # List all files in the directory
        if file.endswith(".json.enc")  # Filter only .json.enc files
    ]

    for file in filenames:
        print(Fore.LIGHTGREEN_EX + f"- {file}")
    print("")


def add_data():
    """Adds new password data into the file"""

    # check if encryption key is present or not
    check_if_aes_key_present(aes_key_path)

    # take the file_name input
    file_name = take_file_name()
    file_path = os.path.join(storage_path, f"{file_name}.json.enc")

    # check if file exists
    if not os.path.exists(file_path):
        print(Fore.LIGHTRED_EX + "File does not exists!")
        return

    aes_key = decrypt_key()  # decrypt the encryption key
    json_data = decrypt_file(file_path, aes_key)  # decrypt the file data

    # create a new object
    new_data = {}
    new_data["key"] = input(Fore.LIGHTCYAN_EX + "Object_Key: ")

    # take other key value pair data
    while True:
        key = input(Fore.BLUE + "key: ")
        if key == "exit":
            break

        value = input(Fore.CYAN + f"{key}: ")
        new_data[key] = value
        print("")

    # Add a new entry to array of object and encrypt the data
    json_data.append(new_data)
    encrypt_file(file_path, json.dumps(json_data), aes_key)
    print("")


def get_data():
    """Get the data stored in the file"""

    # check if encryption key is present or not
    check_if_aes_key_present(aes_key_path)

    file_name = take_file_name()
    file_path = os.path.join(storage_path, f"{file_name}.json.enc")

    if not os.path.exists(file_path):
        print(Fore.LIGHTRED_EX + "File Does not exists!")
        return

    aes_key = decrypt_key()
    json_data = decrypt_file(file_path, aes_key)

    object_key = input(Fore.LIGHTCYAN_EX + "Object_Key: ")
    regex = re.compile(object_key, re.IGNORECASE)

    result = [data for data in json_data if regex.search(data["key"])]
    print(Fore.LIGHTBLACK_EX + json.dumps(result, indent=4, separators=(",", ": ")))
    print("")


def get_object_list():
    """Get list of object ids present in the file."""

    # check if encryption key is present or not
    check_if_aes_key_present(aes_key_path)

    file_name = take_file_name()
    file_path = os.path.join(storage_path, f"{file_name}.json.enc")

    if not os.path.exists(file_path):
        print(Fore.LIGHTRED_EX + "File Does not exists!")
        return

    # Decrypt the file data
    aes_key = decrypt_key()
    json_data = decrypt_file(file_path, aes_key)

    # Get the list of keys
    object_keys = [obj.get("key") for obj in json_data]

    # Display data
    print(Fore.LIGHTGREEN_EX + f"File: {file_name}------------------------------")
    for key in object_keys:
        print(Fore.LIGHTGREEN_EX + f"- {key}")
    print("")

