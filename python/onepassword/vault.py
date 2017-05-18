"""
Author: Sean Richardson
Email: richasea<at>gmail.com
Description: A class to encapsulate access to 1Password vaults.
"""

import glob
import os
import json

class Vault(object):
    """
    Encapsulation of a 1Password vault.
    """

    def __init__(self, path):
        self._path = path
        self._accounts = dict()
        self._load_accounts()

    def _load_accounts(self):
        "Loads the account json files"
        data_dir = "data"
        vault_dir = "default"
        account_wild = "*.1password"
        accounts_glob = os.path.join(self._path, data_dir, vault_dir, account_wild)
        accounts = glob.glob(accounts_glob)
        for account in accounts:
            with open(account) as stream:
                contents = json.load(stream)
                name = contents["title"]
                self._accounts[account] = name

    @property
    def path(self):
        "The vault path"
        return self._path

    @property
    def accounts(self):
        "Accounts stored in the vault"
        return self._accounts.values()
