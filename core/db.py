import os
import platform
import sqlite3

directory = {
    "Linux": os.path.expanduser("~/.local/share/pm/"),
    "Windows": os.path.expanduser("~\\AppData\\pm\\"),
}
dir = directory.get(platform.system())
db_path = os.path.join(dir, "db.db")

def create_database():
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute(
        """ CREATE TABLE
                    credential (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account text,
                    username text,
                    password text,
                    website text,
                    email text,
                    notes text
        ) """
    )

    cur.execute(
        """ CREATE TABLE
                    key (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    credential_id int,
                    key text,
                    FOREIGN KEY(credential_id) REFERENCES credential(id)
        ) """
    )
    con.commit()
    con.close()
