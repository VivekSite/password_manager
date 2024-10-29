import os
from os import urandom
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from utils import getConfigData, exitHandler

# Get the configuration data
json_data = getConfigData()

# Get the path of public key
public_key_path = json_data.get("public_key_path")

if public_key_path is None:
    exitHandler("Public key path is not configured!")

# redefine the variable with expanded path
public_key_path = os.path.expanduser(public_key_path)

# Perform necessary validations
if not os.path.exists(public_key_path):
    exitHandler(f"Public key not found! {public_key_path}")

if os.path.getsize(public_key_path) == 0:
    exitHandler(f"Public key file is empty! {public_key_path}")

# AES block_size
block_size = AES.block_size


def encrypt_file(file_path, file_data, key):
    """Encodes the file data, Encrypts it and writes the data into file"""

    # Generate a random initialization vector (IV)
    iv = urandom(block_size)

    # Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad the plaintext to be a multiple of block size
    padded_data = pad(file_data.encode("utf-8"), block_size)

    # Encrypt the data
    ciphertext = cipher.encrypt(padded_data)

    # Write the IV + ciphertext to the output file
    with open(file_path, "wb") as f:
        f.write(iv + ciphertext)


def encrypt_aes_key(aes_key_path, aes_key):
    """Encrypts the encryption key with public key"""

    # Load the public key from the file
    with open(public_key_path, "rb") as f:
        public_key = load_pem_public_key(f.read())

    # Encrypt the AES key with the public key
    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # Save the encrypted AES key to a file
    with open(aes_key_path, "wb") as f:
        f.write(encrypted_aes_key)
