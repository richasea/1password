"""
Author: Sean Richardson
Email: richasea<at>gmail.com
Description: A class to encapsulate access to 1Password vaults.
"""

import base64
import getpass
import glob
import hashlib
import os
import json

from pbkdf2 import PBKDF2
from Crypto.Cipher import AES

from onepassword.plist import PropertyList

class Vault(object):
    """
    Encapsulation of a 1Password vault.
    """

    def __init__(self, path):
        self._path = path
        self._items = dict()
        self._properties = None
        self._encryption_key = None

        self._load_properties()
        self._load_items()

    def _load_properties(self):
        "Loads vault properties"
        properties_file = os.path.join(self._path, "data", "default", "1password.keys")
        self._properties = PropertyList()
        self._properties.load(properties_file)

    def _load_items(self):
        "Loads the account json files"
        data_dir = "data"
        vault_dir = "default"
        account_wild = "*.1password"
        accounts_glob = os.path.join(self._path, data_dir, vault_dir, account_wild)
        accounts = glob.glob(accounts_glob)
        for account in accounts:
            with open(account) as stream:
                contents = json.load(stream)
                item_type = contents["typeName"]
                if not item_type in self._items:
                    self._items[item_type] = list()
                self._items[item_type].append(contents)

    def decrypt(self):
        """
        Decrypts the password vault.
        """
        password = getpass.getpass("Password: ")
        for datum in self._properties.data["list"]:
            if datum["level"] == "SL5":
                iterations = datum["iterations"]
                data = datum["data"]
                (salt, data) = Vault._parse_data(data)
                password_hash = PBKDF2(password, salt, iterations).read(32)
                (key, init_vector) = (password_hash[:16], password_hash[16:])
                aes = AES.new(key, AES.MODE_CBC, init_vector)

                encryption_key = aes.decrypt(data)[:1024]

                (vsalt, vdata) = Vault._parse_data(datum["validation"])
                (vkey, viv) = Vault._gen_key_iv(encryption_key, vsalt)
                aes = AES.new(vkey, AES.MODE_CBC, viv)
                vdata = aes.decrypt(vdata)[:1024]

                if vdata == encryption_key:
                    self._encryption_key = encryption_key
                    return True
        return False

    def decrypt_item(self, lookval):
        """
        Decrypts a value in the vault.
        """
        for _, items in self._items.items():
            for item in items:
                if item["uuid"] == lookval:
                    data = item["encrypted"]
                    (salt, data) = Vault._parse_data(data)
                    #pylint: disable=invalid-name
                    (key, iv) = Vault._gen_key_iv(self._encryption_key, salt)
                    aes = AES.new(key, AES.MODE_CBC, iv)
                    plain = aes.decrypt(data)
                    padding = plain[-1]
                    inverse_padding = -1 * padding
                    plain = plain[:inverse_padding]
                    strval = plain.decode("utf-8", "ignore")
                    return json.loads(strval)

        raise RuntimeError("Item not found!")

    @staticmethod
    def _parse_data(data):
        """
        Parse account data.
        """
        data = base64.b64decode(data.strip())
        if data[:8] == b"Salted__":
            (salt, data) = (data[8:16], data[16:])
            return (salt, data)
        else:
            raise NotImplementedError("Only salted data is supported")

    @staticmethod
    def _gen_key_iv(password, salt):
        """
        Generates an IV and key given a password and salt.
        """
        rounds = 2
        data = password + salt
        md5s = [hashlib.md5(data)]
        result = md5s[0].digest()
        for i in range(1, rounds):
            new_md5 = hashlib.md5(md5s[i-1].digest() + data)
            md5s.append(new_md5)
            result = result + new_md5.digest()
        key = result[:16]
        the_iv = result[16:]
        return (key, the_iv)

    def __getitem__(self, header):
        """
        Takes a header and gets all items that match.
        """
        key = Vault._header_to_key(header)
        if key not in self._items:
            return []

        pairs = [(i["title"], i["uuid"]) for i in self._items[key]]
        pairs.sort(key=lambda p: p[0].lower())
        return pairs

    @property
    def path(self):
        "The vault path"
        return self._path

    @property
    def headers(self):
        "Vault contents headers"
        keys = self._items.keys()
        blacklist = ["system.folder.Regular"]
        keys = [key for key in keys if key not in blacklist]
        mapped = [Vault._key_to_header(k) for k in keys]
        mapped.sort()
        return mapped

    @staticmethod
    def _key_to_header(key):
        lookup = {
            "webforms.WebForm" : "Logins",
            "passwords.Password": "Passwords",
            "wallet.onlineservices.GenericAccount" : "Generic Accounts",
            "wallet.financial.CreditCard" : "Credit Cards",
            "wallet.computer.License" : "Licenses",
            "securenotes.SecureNote" : "Notes",
            "system.folder.Regular" : "Folders"
            }
        if key in lookup:
            return lookup[key]
        return "?"

    @staticmethod
    def _header_to_key(header):
        lookup = {
            "Logins" : "webforms.WebForm",
            "Passwords" : "passwords.Password",
            "Generic Accounts" : "wallet.onlineservices.GenericAccount",
            "Credit Cards" : "wallet.financial.CreditCard",
            "Licenses" : "wallet.computer.License",
            "Notes" : "securenotes.SecureNote",
            "Folders" : "system.folder.Regular",
            }
        if header in lookup:
            return lookup[header]
        return "?"

    @property
    def accounts(self):
        "Accounts stored in the vault"
        return []
