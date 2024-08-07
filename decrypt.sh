#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 <filename.gpg>"
  exit 1
fi

filename="${1%.gpg}"
gpg -d --cipher-algo AES256 "$1" 2>/dev/stdout

if [ $? -eq 0 ]; then
  printf "\nFile '$1' decrypted successfully."
else
  printf "Error: Decrypting '$1' failed."
fi
