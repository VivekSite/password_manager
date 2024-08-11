# Password Manager
- This is a CLI application which stores and manages your passwords in a encrypted way.
- All the passwords are stored in `JSON` structure.
- Encryption algorithms used to encrypt the file is `AES256` by using `GnuPG`.
- Example password structure:
```
  [
    {
      "key": "LinkedIn",
      "email": "example@example.com",
      "password": "XXXXXXXXX",
      ...
    },
    {
      "key": "GitHub",
      "email": "example@example.com",
      "password": "example@example.com",
      ...
    }
  ]
```
- The Example of stored password:
```
-----BEGIN PGP MESSAGE-----

jA0ECQMIf3kcNcsXx3Tw0ngBEwQZlGzSOa8N+Q5I+vPBBwRUHz3Cyxwr1ZMS8SnS
Q6oOH2YdDphTs/8r2KBzwSSOcrlNhh58Gob5XjAY2yfLFkr+ec0pq2oHWnEo7KyY
T6PU7GzFXMUVhsvBIRGa0Kyd0ZLFmiXJipYRFysmDbHJ/1l1iY+LcwU=
=pHrr
-----END PGP MESSAGE-----
```
- This Password is stored in the `.pass_storage` directory in the root directory.

# Setup the project
- Make sure that you have `GnuPG` installed on you system
- Enter this command in terminal to check if it installed or not `gpg --version`
- If Not then install it
```
// For Linux
sudo apt install gnupg

// For MacOS
sudo brew install gnupg

```
- Clone the repository
```
git clone https://github.com/VivekSite/password_manager.git
```
- Create a virtual environment
```
python3 -m venv .venv
```
- Activate the virtual environment
```
. .venv/bin/activate
```
- Install all the dependencies
```
pip install -r requirements.txt
```
- Now run the program
```
chmod +x start.sh
./start.sh
```

# How To Use
- After running the program you will see these options:
```
❯ ./start.sh
1. Create new file
2. Add data
3. Get data
4. exit

Select from above:
```
- select one of them and enter
## Option 1
- After selecting option 1 you will be prompted to enter File name.
```
Select from above: 1

File_Name: test
```
- This will creates a new file in directory `.pass_storage` to store the password
- After the file name you have to create a passphrase to encrypt the file
```
File_Name: test
Passphrase: 
Enter a passphrase again:
```
- Just create a new strong passphrase you will need it when accessing the password again.
- Password is hidden by default.

## Option 2
- With second option you can add data objects to the file you just created
- Select option 2 and enter the file name in which you wanted to add this data and enter the passphrase to access that file.
```
Select from above: 2

File_Name: test
Passphrase:
```
- After entering the currect passphrase you can add data.
- First it will ask you to enter `Object_Key`.
- After that you can add data in `key: value` pairs.
```
File_Name: test
Passphrase: 
Object_Key: GitHub

key: email
email: example@gmail.com

key: password
password: This_Is_Password        

key: exit    // enter this to exit
```
- Here in the example you can see I'm adding the `password` and `email` for my github account.
- To `Exit and Save` the data you have to enter `exit` as key.

## Option 3
- Using option 3 you can view your stored data by using the `Object_Key`
- And of course you have to enter file name and passphrase to access it.
```
Select from above: 3

File_Name: test
Passphrase: 
Key_Name: GitHub
{
    "key": "GitHub",
    "email": "example@gmail.com",
    "password": "This_Is_Password"
}
```
- This is how you can see the stored password