"""required imports"""

import getpass
import os
import gnupg
from colorama import init, Fore, Style

init()

path = os.path.join(os.getcwd(), "../.gnupg")
data_path = os.path.join(os.getcwd(), ".pass_storage")
gpg = gnupg.GPG(gnupghome=path)


def encrypt_file():
    """Function to encrypt the file"""
    file_name = input(Fore.LIGHTYELLOW_EX + "File_Name: ")
    input_file = os.path.join(data_path, file_name)
    output_file = os.path.join(data_path, f"{file_name}.gpg")

    if not os.path.exists(input_file):
        print(Fore.LIGHTRED_EX + f"File with name {input_file} doesn't exists!")
        return

    passphrase = getpass.getpass(Fore.LIGHTBLACK_EX + "Passphrase: ")
    while True:
        verify_passphrase = getpass.getpass("Enter a passphrase again: ")
        if passphrase == verify_passphrase:
            break

        print(Fore.LIGHTRED_EX + "Passphrase Didn't matched!")
        print(Style.RESET_ALL)

    gpg.encrypt_file(
		input_file,
		recipients=None,
		symmetric="AES256",
		passphrase=passphrase,
		output=output_file,
	)

encrypt_file()
