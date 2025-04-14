from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

BLOCK_SIZE = 16

def pad(data):
    return data + b"\0" * (BLOCK_SIZE - len(data) % BLOCK_SIZE)

def unpad(data):
    return data.rstrip(b"\0")

def encrypt_aes(data, key):
    key = key.ljust(BLOCK_SIZE, '0').encode()
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data.encode()))
    return base64.b64encode(iv + encrypted).decode()

def decrypt_aes(ciphertext, key):
    key = key.ljust(BLOCK_SIZE, '0').encode()
    raw = base64.b64decode(ciphertext)
    iv = raw[:BLOCK_SIZE]
    encrypted = raw[BLOCK_SIZE:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted)).decode()
