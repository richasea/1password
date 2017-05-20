# 1Password
## Introduction
I was quite frustrated at not having a 1Password client for my Linux laptop and Raspberry Pi so I decided to have a go at writing one.
This software is quite basic in that it will only open local 1Password vaults.

Usual warnings apply: This software is not supported by AgileBits.
Although I have taken care not to make stupid mistakes, this software is probably insecure and I accept no responsibility for your account getting compromised as a result of you using it. **You install this software at your own risk.**

## Installation
First install dependencies:
```bash
pip install -r requirements.txt
```
And then install the software itself.
```bash
sudo ./setup.py install
```

## Usage:
First create a config file in your home directory called '.1password'
it should look similar to this:
```
[vault]
path=/path/to/password.agilekeychain
```

You can then run 1password from the command line.
You will be prompted to enter a password, once this is complete you will be presented with a gui. I use that term loosely.
Use up down left and right to select the entry, and press enter to view it.
Use ESC to close the window.
Use 'Q' to exit the application.
