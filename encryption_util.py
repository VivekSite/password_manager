import os
from os import urandom
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import json

# Paths for keys and storage
config_file_path = os.path.join(os.getcwd(), ".config")
with open(config_file_path, "r") as file:
    json_data = json.load(file)

public_key_path = os.path.expanduser(json_data.get("public_key_path"))
aes_key_path = json_data.get("aes_key")

block_size = AES.block_size

def encrypt_file(file_path, file_data, key):
    # Generate a random initialization vector (IV)
    iv = urandom(block_size)
    
    # Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad the plaintext to be a multiple of block size
    padded_data = pad(file_data.encode("utf-8"), block_size)

    # Encrypt the data
    ciphertext = cipher.encrypt(padded_data)

    # Write the IV + ciphertext to the output file
    with open(file_path, 'wb') as f:
        f.write(iv + ciphertext)


def encrypt_aes_key(aes_key_path, aes_key):
    # Step 1: Load the public key from the file
    with open(public_key_path, 'rb') as f:
        public_key = load_pem_public_key(f.read())

    # Step 2: Encrypt the AES key with the public key
    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Step 3: Save the encrypted AES key to a file
    with open(aes_key_path, 'wb') as f:
        f.write(encrypted_aes_key)

