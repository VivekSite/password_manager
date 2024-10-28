import os
from os import urandom
from colorama import init, Fore
from utils import take_file_name
from decryption_util import decrypt_file, decrypt_key
from encryption_util import encrypt_file
import json
import re 

#Path for storage
config_file_path = os.path.join(os.getcwd(), ".config")
with open(config_file_path, "r") as file:
    json_data = json.load(file)

data_path = json_data.get("storage_path")

def create_new_file():
    file_name = take_file_name()
    file_path = os.path.join(data_path, f"{file_name}.json.enc")
    
    key = decrypt_key()
    encrypt_file(file_path, json.dumps([]), key)
    print(Fore.LIGHTMAGENTA_EX + f"New file created successfully: {file_name}\n")


def print_files():
    filenames = [
        os.path.splitext(os.path.splitext(file)[0])[0]  # Remove the extension
        for file in os.listdir(data_path)  # List all files in the directory
        if file.endswith(".json.enc")  # Filter only .json files
    ]
    
    for file in filenames: 
        print(f"- {file}")
    print("")


def add_data():
    file_name = take_file_name()
    file_path = os.path.join(data_path, f"{file_name}.json.enc")
    
    if not os.path.exists(file_path):
        print(Fore.LIGHTRED_EX + "File does not exists!")
        return

    aes_key = decrypt_key()
    json_data = decrypt_file(file_path, aes_key)
    
    # create a new object 
    new_data = {} 
    new_data["key"] = input(Fore.LIGHTYELLOW_EX + "Object_Key: ")
    print("")

    # take other key value pair data 
    while True:
        key = input(Fore.BLUE + "key: ")
        if key == "exit":
            break

        value = input(Fore.CYAN + f"{key}: ")
        new_data[key] = value
        print("")

    json_data.append(new_data)
    encrypt_file(file_path, json.dumps(json_data), aes_key)


def get_data():
    file_name = take_file_name()
    file_path = os.path.join(data_path, f"{file_name}.json.enc")
    
    if not os.path.exists(file_path):
        print(Fore.LIGHTRED_EX + "File Does not exists!")
        return
    
    aes_key = decrypt_key()
    json_data = decrypt_file(file_path, aes_key)

    object_key = input(Fore.LIGHTYELLOW_EX + "Object_Key: ")
    regex = re.compile(object_key, re.IGNORECASE)

    result = [data for data in json_data if regex.search(data["key"])]
    print(Fore.LIGHTBLACK_EX + json.dumps(result, indent=4, separators=(",", ": ")))

