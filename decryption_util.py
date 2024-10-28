import os
from os import urandom
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import json

# Paths for keys and storage
config_file_path = os.path.join(os.getcwd(), ".config")
with open(config_file_path, "r") as file:
    json_data = json.load(file)

private_key_path = os.path.expanduser(json_data.get("private_key_path"))
aes_key_path = json_data.get("aes_key_path")

block_size = AES.block_size

def decrypt_file(file_path, key):
    # Read the input file (IV + ciphertext)
    with open(file_path, 'rb') as f:
        iv = f.read(block_size)  # First 16 bytes are the IV
        ciphertext = f.read()    # Remaining bytes are the ciphertext

    # Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the ciphertext
    padded_data = cipher.decrypt(ciphertext)

    # Unpad the decrypted data
    decrypted_data = unpad(padded_data, block_size)
    decrypted_json_data = decrypted_data.decode("utf-8")

    return json.loads(decrypted_json_data)

def decrypt_key():
    # Step 1: Load the private key from the PEM file
    with open(private_key_path, 'rb') as f:
        private_key_data = f.read()

    private_key = load_pem_private_key(private_key_data, password=None)

    # Step 2: Load the encrypted AES key from the binary file
    with open(aes_key_path, 'rb') as f:
        encrypted_aes_key = f.read()

    # Step 3: Decrypt the AES key using the private key
    decrypted_aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_aes_key


