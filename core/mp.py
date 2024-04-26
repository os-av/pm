import os
import hashlib
import platform

class MasterPassword:
    def __init__(self):
        directory = {
            "Linux": os.path.expanduser("~/.local/share/pm/"),
            "Windows": os.path.expanduser("~\\AppData\\pm\\"),
        }
        self.dir = directory.get(platform.system())

        self.mp_path = os.path.join(self.dir, "mp")

    def create_master_password(self, password):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
    
        password_bytes = password.encode("utf-8")
        hash = hashlib.sha256(password_bytes).hexdigest()

        with open(self.mp_path, "w") as file:
            file.write(hash)

    def verify_master_password(self, password):
        with open(self.mp_path, "r") as file:
            hash = file.read()

        password_bytes = password.encode("utf-8")
        password_hash = hashlib.sha256(password_bytes).hexdigest()

        if hash == password_hash:
            return True
        return False

    def master_password_setup_required(self):
        if not os.path.exists(self.mp_path):
            return True
        return False
