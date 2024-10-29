import os
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from utils import getConfigData, exitHandler


# Get the configuration data
json_data = getConfigData()

# Get the path of encryption key and private key
private_key_path = json_data.get("private_key_path")
aes_key_path = json_data.get("aes_key_path")

if private_key_path is None:
    exitHandler("Private key path is not configured!")

if aes_key_path is None:
    exitHandler("Encryption key path is not configured!")

# redefine the variable with expanded path
private_key_path = os.path.expanduser(private_key_path)
aes_key_path = os.path.expanduser(aes_key_path)

# Perform necessary validations
if not os.path.exists(private_key_path):
    exitHandler(f"Private key not found! {private_key_path}")

if not os.path.exists(aes_key_path):
    exitHandler(f"Encryption key not found! {aes_key_path}")

if os.path.exists(private_key_path) and os.path.getsize(private_key_path) == 0:
    exitHandler(f"Private key file is empty! {private_key_path}")

if os.path.exists(aes_key_path) and os.path.getsize(aes_key_path) == 0:
    exitHandler(f"Encryption key file is empty! {aes_key_path}")

# AES block_size
block_size = AES.block_size


def decrypt_file(file_path, key):
    """Decrypts the file data at given path and returns it"""

    # Read the input file (IV + ciphertext)
    with open(file_path, "rb") as f:
        iv = f.read(block_size)  # First 16 bytes are the IV
        ciphertext = f.read()  # Remaining bytes are the ciphertext

    # Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the ciphertext
    padded_data = cipher.decrypt(ciphertext)

    # Decode and Unpad the decrypted data
    decrypted_data = unpad(padded_data, block_size)
    decrypted_json_data = decrypted_data.decode("utf-8")

    return json.loads(decrypted_json_data)


def decrypt_key():
    """Decrypts the encryption key with private key and returns the decrypted key"""

    # Load the private key from the PEM file
    with open(private_key_path, "rb") as f:
        private_key_data = f.read()

    private_key = load_pem_private_key(private_key_data, password=None)

    # Load the encrypted AES key from the binary file
    with open(aes_key_path, "rb") as f:
        encrypted_aes_key = f.read()

    # Decrypt the AES key using the private key
    decrypted_aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return decrypted_aes_key
