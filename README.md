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
