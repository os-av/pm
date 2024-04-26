import sqlite3
import os
from core.db import db_path
from core.encryption import encrypt, decrypt, derive_key

class PasswordManager():
    def __init__(self):
        self.key = ""

    def create_new_credential(self, account, username, password, 
                              website="", email="", notes=""):
        """
        Adds a new credential to the database, along with its generated
        key. The new credential is encrypted using the encrypted key and
        the credential key is encrypted with the master key.
        """
        credential_key = derive_key(os.urandom(16), os.urandom(16))
        encrypted_key = encrypt(credential_key, self.key)

        account  = encrypt(account.encode(), credential_key)
        username = encrypt(username.encode(), credential_key)
        password = encrypt(password.encode(), credential_key)
        website  = encrypt(website.encode(), credential_key)
        email    = encrypt(email.encode(), credential_key)
        notes    = encrypt(notes.encode(), credential_key)

        con = sqlite3.connect(db_path)
        cur = con.cursor()

        cur.execute(
        """ INSERT INTO
            credential (account, username, password,
                        website, email, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        , (account, username, password, website, email, notes))

        cur.execute(
        """ INSERT INTO
            key (key, credential_id)
            VALUES (?, ?)
        """
        , (encrypted_key, cur.lastrowid))

        con.commit()
        con.close()

    def read_all_credentials(self):
        """
        Reads all credentials from the database. Returns a list of all
        decrypted credentials.
        """
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        cur.execute(
        """ SELECT c.*, k.key
            FROM credential c
            JOIN key k ON c.id = k.credential_id
        """)
        rows = cur.fetchall()
        con.close()

        credential_list = []
        for row in rows:
            credential_key = decrypt(row[-1], self.key) 
            data = list(row[0:7])
            for i in range(1, len(data)):
                data[i] = decrypt(data[i], credential_key).decode()
            credential_list.append(data)
        return credential_list

    def read_credential_by_id(self, id):
        """
        Returns a credential from its ID in the database.
        """
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        cur.execute(
        """ SELECT c.*, k.key
            FROM credential c
            JOIN key k ON c.id = k.credential_id
            WHERE c.id = ?
        """
        , (id,))
        row = cur.fetchone()

        if not row:
            return None
            
        credential_key = decrypt(row[-1], self.key) 
        data = list(row[0:7])
        for i in range(1, len(data)):
            data[i] = decrypt(data[i], credential_key).decode()
        return data
        
    def read_credential_by_account(self, account):
        """
        Finds a credential in the database by it's account name.
        """
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        cur.execute(
        """ SELECT c.*, k.key
            FROM credential c
            JOIN key k ON c.id = k.credential_id
        """)
        rows = cur.fetchall()
        con.close()

        data = None
        for row in rows:
            credential_key = decrypt(row[-1], self.key)
            if decrypt(row[1], credential_key).decode() == account:
                data = row
                break

        if not data:
            return None

        data = list(data[0:7])
        for i in range(1, len(data)):
            data[i] = decrypt(data[i], credential_key).decode()
        return data

    def update_credential_by_id(self, col, id, data):
        """
        Updates a credential on the supplied ID and column.
        """
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        cur.execute(
        """ SELECT key
            FROM key
            WHERE id = ?
        """
        , (id,))
        row = cur.fetchone()
        if not row:
            return None

        credential_key = decrypt(row[0], self.key)
        data = encrypt(data.encode(), credential_key)

        cur.execute(
        f""" UPDATE credential 
             SET {col} = ? 
             WHERE id = ?
        """
        , (data, id,))

        con.commit()
        con.close()
    
    def delete_credential_by_id(self, id):
        """
        Delete a credential from it's ID.
        """
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        cur.execute("DELETE FROM credential WHERE id = ?", (id,))
        cur.execute("DELETE FROM key WHERE id = ?", (id,))

        con.commit()
        con.close()

    def delete_credential_by_account(self, account):
        """
        Delete a credential from the DB through its give account name.
        """
        id = self.read_credential_by_account(account)[0]
        self.delete_credential_by_id(id)
    
    def get_password_of_credential(self, account):
        """
        Returns the password of an individual credential.
        """
        credential = self.read_credential_by_account(account)
        if credential:
            return credential[3]
        return None

    def set_key(self, password):
        """
        Sets the master key.
        """
        self.key = derive_key(password)
