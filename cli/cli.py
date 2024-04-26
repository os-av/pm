import argparse
import getpass
import webbrowser
import pyperclip 
from tabulate import tabulate
from core.db import create_database
from core.settings import Settings
from core.mp import MasterPassword
from core.pm import PasswordManager
from core.generator import Generator

class CLI:
    """
    CLI utility.
    """
    def __init__(self):
        self.parser = self.create_parser()
        self.args = self.parser.parse_args()

        self.pm = PasswordManager()
        self.mp = MasterPassword()
        self.settings = Settings()

    def run(self):
        if self.args.init:
            self.init()
        elif self.mp.master_password_setup_required():
            print("No master password found. Run 'pm --init' to setup files.")

        elif self.args.create:
            self.create()
        elif self.args.update:
            self.update()
        elif self.args.fetch:
            self.fetch()
        elif self.args.list:
            self.list_credentials()
        elif self.args.delete:
            self.delete()
        elif self.args.go:
            self.go()
        else:
            self.parser.print_help()

    def copy(self):
        if not self.verify_and_set():
            return
        account = self.pm.read_credential_by_account(self.args.copy)

        if account is None:
            print("Account not found.")
            return

        password = account[3]
        pyperclip.copy(password)
        print("Copied password to clipboard.")

    def go(self):
        if not self.verify_and_set():
            return

        account = self.pm.read_credential_by_account(self.args.go)

        if account is None:
            print("Account not found.")
            return

        password = account[3]
        pyperclip.copy(password)
        print("Copied password to clipboard. Opening URL if stored...")

        url = account[4]
        if len(url) > 0:
            if url[:8] != 'https://':
                url = 'https://' + url
            webbrowser.open(url)

    def delete(self):
        if not self.verify_and_set():
            return

        credential = self.pm.read_credential_by_account(self.args.delete)
        if credential is None:
            print("Account not found.")
            return

        self.pm.delete_credential_by_id(credential[0])
        print("Credential removed.")

    def list_credentials(self):
        if not self.verify_and_set():
            return

        credentials = self.pm.read_all_credentials()
        for cred in credentials:
            cred.pop(3) # Remove password
            cred.pop(-1) # Remove notes

        print(tabulate(credentials, 
            headers=["ID", "Account", "Username", "Website", "Email"], 
            tablefmt="grid"))

    def fetch(self):
        if not self.verify_and_set():
            return

        cred = self.pm.read_credential_by_account(self.args.fetch)
        if cred is None:
            print("Account does not exist.")
            return

        cred.pop(3) # Remove password
        cred.pop(-1) # Remove notes
        print(tabulate([cred], 
            headers=["ID", "Account", "Username", "Website", "Email"], 
            tablefmt="grid"))

    def update(self):
        if not self.verify_and_set():
            return

        db_cols = ["account", "username", "password", "website", "email"]
        account, column, value = self.args.update

        if column not in db_cols:
            print("Column not in DB. Check 'pm -h' for values.")

        cred = self.pm.read_credential_by_account(account)
        if cred is None:
            print("Account does not exist.")
            return

        self.pm.update_credential_by_id(column, cred[0], value)
        print("Credential updated.")

    def create(self):
        if not self.verify_and_set():
            return

        account, username, website, email = self.args.create
        generator = Generator()
        password = generator.generate_password()

        if self.pm.read_credential_by_account(account):
            print("Account already exists.")
            return

        self.pm.create_new_credential(account, username, password, website, email)
        print("New credential added.")

    def init(self):
        if not self.mp.master_password_setup_required():
            print("Master password already found. Cancelling.")
            return

        p1 = getpass.getpass("Enter a master password: ")
        p2 = getpass.getpass("Confirm master password: ")

        if p1 != p2:
            print("Passwords did not match.")
            return
        
        create_database()
        self.settings.create_settings()
        self.mp.create_master_password(p1)
        print("Setup complete. See 'pm -h' for usage.")

    def verify_and_set(self):
        password = getpass.getpass("Enter master password: ")
        if not self.mp.verify_master_password(password):
            print("Password was incorrect.")
            return False

        self.pm.set_key(password.encode())
        return True

    def create_parser(self):
        parser = argparse.ArgumentParser(description="pm")

        parser.add_argument(
            "--init", 
            action="store_true", 
            help="setup")

        parser.add_argument(
            "--create", 
            nargs=4,
            metavar=("ACCOUNT", "USERNAME", "WEBSITE", "EMAIL"),
            help="create a new credential, a random password is generated")

        parser.add_argument(
            "--delete", 
            metavar="ACCOUNT",
            help="delete a credential")

        parser.add_argument(
            "--update", 
            nargs=3,
            metavar=("ACCOUNT", "DETAIL", "VALUE"),
            help="""update a credential, requires the account name, the 
            details to update (account, username, password, website, or email) 
            and the value.""")

        parser.add_argument(
            "--fetch", 
            metavar="ACCOUNT",
            help="fetch details of the specified credential")

        parser.add_argument(
            "--list", 
            action="store_true", 
            help="list all credential details")

        parser.add_argument(
            "--copy", 
            metavar="ACCOUNT",
            help="copy a password to the clipboard")

        parser.add_argument(
            "--go", 
            metavar="ACCOUNT",
            help="""copy password, if the URL for the account is stored it will
            be opened in the default browser.""")
        return parser
