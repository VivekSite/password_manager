# Password Manager
- This is a CLI application which stores and manages your passwords in a encrypted form.
- I'm using hybrid Encryption to encrpt the file data.
- Generate the AES256 key and encrypt all the file data with this key.
- Encrypt this AES256 key with public key. which can only be decrypted the respective private key.

# Setup the project
- Step 1: Clone the repository
```
git clone https://github.com/VivekSite/password_manager.git
```
- Step 2: Install dependencies
```
pip install -r requirement.txt
```
- Step 3: Now run the program
```
./start.sh
```

# How To Use
- Before running the program make sure you have your configuration file ready.
- Create a .config file `touch .config` and put this configurations.
```
{
  "private_key_path": "~/password_manager/private_key.pem",
  "public_key_path": "~/password_manager/public_key.pem",
  "storage_path": "~/password_manager/.storage",
  "aes_key_path": "~/password_manager/aes_key.bin"
}
```
- here we have to configure the path to private and public key(we will create it later).
- storage_path is the location of directory where you want to store the files.
- aes_key_path is path to you encryption key(we will create it later).

## Generate private and public keys
- Run following command to generate keys. Keys will get stored on configured path.
```
./gen-private-key.sh
```

## Generate encryption key
- Run following command to generate encryption key. It will get stored on configured path in encrypted format.
```
./gen-aes-key.sh
```

## Run the program 
```
./start.sh
```
- After running the program you will see these options:
```
1. Create new file
2. List object keys
3. List files
4. Add data
5. Get data
6. Exit
Select from above:
```
- select one of them and enter
## Option 1: Create new file
- After selecting option 1 you will be prompted to enter File name.
```
Select from above: 1,
File name: test
New file created successfully: test
```
- This will creates a new file in directory `.storage` to store the passwords.

## Option 3: List files
- This option will show the list of files which we have created so far.
```
Select from above: 3
- test2
- test
- vivek
```

## Option 4: Add data
- With this option you can add data objects to the file you just created.
- Select option 4 and enter.
- It will ask for file name so enter the file name in which you wanted to add data object.
- Now it will ask you to enter `Object_Key`.
- After that you can add data in `key: value` pairs.
```
Select from above: 4
File name: test
Object_Key: youtube
key: email
email: example@gmail.com

key: password
password: example@1234

key: mobile
mobile: 1234567890       

key: exit    // enter this to exit
```
- Here in the example you can see I'm adding the `email`, `password` and `mobile` for my youtube account.
- To `Exit and Save` the data, you have to enter `exit` as key.

## Option 2: List object keys
- By this option you see the list of Object_Keys preset in the file.
```
Select from above: 2
File name: test                                                                     
File: test------------------------------                                            
- linkedin
- youtube
```
- As you can see I have added two objects in the file test.



## Option 5: Get data
- Using option 5 you can view your stored data by using the `Object_Key`
- Object_Key search is case insensitive and it will return all the matching Objects.
```
Select from above: 5
File name: test
Object_Key: youtube
[
    {
        "key": "youtube",
        "email": "example@gmail.com",
        "password": "example@1234",
        "mobile": "1234567890"
    }
]

```
- This is how you can see the stored password

## Option 6: Exit
- Exit the program.