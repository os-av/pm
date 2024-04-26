import string
import secrets
from core.settings import Settings

class Generator:
    def __init__(self):
        self.settings = Settings()

    def generate_password(self):
        chars = string.ascii_lowercase + string.digits
        pwd = ""

        if self.settings.read_boolean_setting("pw_gen", "upper"):
            chars += string.ascii_uppercase
        if self.settings.read_boolean_setting("pw_gen", "other"):
            chars += string.punctuation

        len = int(float(self.settings.read_setting("pw_gen", "len")))

        for _ in range(len):
            pwd += secrets.choice(chars)
        return pwd
