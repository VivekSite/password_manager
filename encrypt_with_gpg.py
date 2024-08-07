"""required imports"""

import os
import gnupg
from colorama import init, Fore, Style

init()

path = os.path.join(os.getcwd(), "../.gnupg")
data_path = os.path.join(os.getcwd(), ".pass_storage")
gpg = gnupg.GPG(gnupghome=path)


def encrypt_with_gpg():
    """Function to encrypt the file"""
    file_name = input(Fore.LIGHTYELLOW_EX + "File_Name: ")
    input_file = os.path.join(data_path, file_name)
    output_file = os.path.join(data_path, f"{file_name}.gpg")

    if not os.path.exists(input_file):
        print(Fore.LIGHTRED_EX + f"File with name {input_file} doesn't exists!")
        return

    print(Style.RESET_ALL)
    status = os.system(f"gpg --symmetric --cipher-algo AES256 -o {output_file} {input_file}")

    if status == 0:
        print(Fore.LIGHTGREEN_EX + "File encypted successfully")
    else:
        print(Fore.LIGHTRED_EX + "Error while encypting file!")

encrypt_with_gpg()
