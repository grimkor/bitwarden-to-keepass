import getpass
import json
from os import environ

import pexpect


class BwFetcher:
    def __init__(self):
        self.DATA = None
        self.USERNAME = environ.get('BW_USERNAME')
        self.PASSWORD = environ.get('BW_PASSWORD')
        self.SESSION = environ.get('BW_SESSION')

    def is_logged_in(self):
        child = pexpect.spawn('bw login')
        response = child.expect(['You are already logged in', 'Email address:'])
        child.close()
        return response == 0

    def unlock(self):
        try:
            child = pexpect.spawn('bw unlock --raw')
            child.expect('Master password:')
            if not self.PASSWORD:
                self.PASSWORD = getpass.getpass(f'Bitwarden master password to unlock vault: ')
            child.sendline(self.PASSWORD)
            lines = child.readlines()
            output: bytes = lines[len(lines) - 1]
            token = output.decode().rstrip('\r\n')
            self.SESSION = token
            child.close()
            print('Vault unlocked.')
        except Exception:
            print('There was a problem unlocking the vault.')

    def login(self):
        try:
            if self.is_logged_in():
                print('Existing Bitwarden session found, unlocking vault.')
                self.unlock()
            else:
                child = pexpect.spawn('bw login --raw')
                child.expect('Email address:')
                if not self.USERNAME:
                    self.USERNAME = input('Email address:')
                child.sendline(self.USERNAME)
                child.expect('Master password:')
                if not self.PASSWORD:
                    self.PASSWORD = getpass.getpass(f'Bitwarden master password for {self.USERNAME}: ')
                child.sendline(self.PASSWORD)
                mfa = child.expect(['Two-step login code:'])
                if mfa == 0:
                    mfa_code = input('Two-step login code:')
                    child.sendline(mfa_code)
                lines = child.readlines()
                output: bytes = lines[len(lines) - 1]
                token = output.decode().rstrip('\r\n')
                self.SESSION = token
                child.close()
                print('Successfully logged in to Bitwarden.')
        except Exception:
            print('There was a problem logging in.')

    def get_items(self):
        if self.SESSION and self.is_logged_in():
            data = pexpect.run(f'bw list items --session {self.SESSION}')
            self.DATA = json.loads(data.decode())
        else:
            self.login()
            if self.is_logged_in():
                data = pexpect.run(f'bw list items --session {self.SESSION}')
                self.DATA = json.loads(data.decode())
                return self.DATA
            else:
                print('There is a problem with the Bitwarden credentials required to perform get_items.')
