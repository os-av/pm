# pm
A simple GUI/CLI password manager written in Python. 
Uses a KDF to generate a master key and encrypts credentials using AES.

# Disclaimer
This project was made in a short time span.
There are no guarantees that you will not lose your data using this project. 
Use a real password manager.

# Requirements
Any Linux distribution.

# Installation
Clone the repository.
```
git clone https://github.com/os-av/pm
```

Install project requirements.
```
cd pm/
pip install -r requirements.txt
```

Add the directory to your PATH or run from the directory with;
```
./pm-gtk
```
or
```
./pm
```
