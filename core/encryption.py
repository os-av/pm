import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def derive_key(password, salt=b'0000'*16):
    """
    Derive a key from input password and salt.
    """
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        salt = salt,
        iterations = 900000,
    )
    key = kdf.derive(password)
    return key

def encrypt(data, key):
    """
    Encrypt data using AES256 using supplied key.
    """
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), 
                    modes.GCM(iv)
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    tag = encryptor.tag
    return iv + ciphertext + tag

def decrypt(data, key):
    """
    Decrypt data using AES256 using supplied key.
    """
    iv = data[0:12]
    ciphertext = data[12:-16]
    tag = data[-16:]
    cipher = Cipher(algorithms.AES(key), 
                    modes.GCM(iv, tag)
    )
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext
