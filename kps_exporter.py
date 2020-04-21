from os import environ
from os.path import exists

import pexpect
import readline
import getpass

readline.set_completer_delims(' \t\n=')
readline.parse_and_bind("tab: complete")

mapping = {
    'username': '--username',
}


class KpsImporter:
    def __init__(self):
        self.file: str or None = environ.get('KEEPASS_FILE')
        self.password: str or None = environ.get('KEEPASS_PASSWORD')
        print(self.file, self.password)
        if self.file and self.password and exists(self.file):
            print('KpsImporter: File and password found from environment variables.')

    def set_target(self, file: str = None, password: str = None):
        if file:
            self.file = file
        if not self.file:
            self.file = input('Path to Keepass database file: ')

        if password:
            self.password = password
        if not self.password:
            self.password = getpass.getpass('Keepass password: ')

    def cmd(self, command):
        child = pexpect.spawn(f'keepassxc-cli {command}')
        child.expect_exact(f'Insert password to unlock {self.file}:')
        child.sendline(self.password)
        return child

    def add(self, title: str = None):
        if title:
            child = self.cmd(' '.join(['add', self.file, f'"{title}"']))
            child.expect(["Successfully added entry*", "Could not create entry with path*"])
            child.terminate()
            return True

    def edit(self, row: dict = None):
        if row:
            cmd_str = ''
            pwd = row['login'].get('password')
            urls = row['login'].get('uris')
            if urls is not None and len(urls):
                url = urls[0]
                cmd_str += f"--url {url.get('uri')}"
            for key in mapping.keys():
                if row['login'].get(key) not in [None, '']:
                    cmd_str += f' {mapping.get(key)} {row["login"].get(key)}'
            if cmd_str:
                if pwd:
                    cmd_str += ' -p'
                child = self.cmd(f'edit {self.file} "{row.get("name")}" {cmd_str}')
                if pwd:
                    child.expect_exact('Enter new password for entry:')
                    child.sendline(pwd or "")
                child.expect("Successfully edited entry*")
                child.terminate()
            return True

    def import_list(self, data: list):
        logins = [record for record in data if record.get('type') == 1]  # 1 === "login"
        total = len(logins)
        count = 1
        print("Importing list to Keepass")
        for login in logins:
            print(f"uploading {count}/{total}", end='\r', flush=True)
            self.add(login.get('name'))
            self.edit(login)
            count += 1
