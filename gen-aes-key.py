import os
from os import urandom
from colorama import init, Fore
from utils import getConfigData, exitHandler
from encryption_util import encrypt_aes_key

# Initialize colorama
init(autoreset=True)

# Get the configuration data
json_data = getConfigData()

# Get the path of encryption key
aes_key_path = json_data.get("aes_key_path")

if aes_key_path is None:
    exitHandler("Encryption key path is not configured!")

# redefine the variable with expanded path
aes_key_path = os.path.expanduser(aes_key_path)

# Perform necessary validations
if os.path.exists(aes_key_path):
    exitHandler(
        f"Encryption key already exists: {aes_key_path}, delete the key to generate new one."
    )

# Generate 32 byte radom key
aes_key = urandom(32)
# Encrypt the key with public key
encrypt_aes_key(aes_key_path, aes_key)

# display completion message
print(Fore.LIGHTGREEN_EX + f"- Key generated successfully: {aes_key_path}")
print(
    Fore.LIGHTGREEN_EX
    + "- The key is encrypted by public key. Keep your private key safe."
)
print(
    Fore.LIGHTGREEN_EX
    + "- All your file is going to be eyncrypted by this key.\n  If you loose it you won't be able to decrypt your files."
)
