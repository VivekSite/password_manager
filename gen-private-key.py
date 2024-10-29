import os
from colorama import init, Fore
from Crypto.PublicKey import RSA
from utils import exitHandler, getConfigData

# Initialize colorama
init(autoreset=True)

# Get the configuration data
json_data = getConfigData()

private_key_path = json_data.get("private_key_path")
public_key_path = json_data.get("public_key_path")

if private_key_path is None:
    exitHandler("Private key path is not configured!")

if public_key_path is None:
    exitHandler("Public key path is not configured!")

# redefine the variable with expanded path
private_key_path = os.path.expanduser(private_key_path)
public_key_path = os.path.expanduser(public_key_path)

if os.path.exists(private_key_path) and os.path.getsize(private_key_path) > 0:
    exitHandler(f"Private key already exists! {private_key_path}")

if os.path.exists(public_key_path) and os.path.getsize(public_key_path) > 0:
    exitHandler(f"Public key already exists! {public_key_path}")


# Generate a 4096-bit RSA private key
key = RSA.generate(4096)


# Export private and public key in PEM format
private_key = key.export_key()
public_key = key.public_key().export_key()


# save the keys to file
with open(private_key_path, "wb") as f:
    f.write(private_key)

with open(public_key_path, "wb") as f:
    f.write(public_key)


# change the file permissions
os.chmod(private_key_path, 0o600)
os.chmod(public_key_path, 0o600)

print(Fore.LIGHTGREEN_EX + f"Private key generated and saved to: {private_key_path}")
print(Fore.LIGHTGREEN_EX + f"Public key generated and saved to: {private_key_path}")
