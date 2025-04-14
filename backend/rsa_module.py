from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os

KEY_SIZE = 2048

def generate_rsa_keys():
    key = RSA.generate(KEY_SIZE)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open("keys/private_key.pem", "wb") as prv_file:
        prv_file.write(private_key)
    with open("keys/public_key.pem", "wb") as pub_file:
        pub_file.write(public_key)

def encrypt_rsa(data, pub_key_file="keys/public_key.pem"):
    with open(pub_key_file, "rb") as file:
        pub_key = RSA.import_key(file.read())
    cipher = PKCS1_OAEP.new(pub_key)
    return base64.b64encode(cipher.encrypt(data.encode())).decode()

def decrypt_rsa(ciphertext, prv_key_file="keys/private_key.pem"):
    with open(prv_key_file, "rb") as file:
        prv_key = RSA.import_key(file.read())
    cipher = PKCS1_OAEP.new(prv_key)
    return cipher.decrypt(base64.b64decode(ciphertext)).decode()
