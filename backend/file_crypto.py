# backend/file_crypto.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

BLOCK_SIZE = 16

def pad(data):
    padding = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([padding]) * padding

def unpad(data):
    padding = data[-1]
    return data[:-padding]

def encrypt_file_aes(input_file, output_file, key_str):
    key = key_str.encode('utf-8')
    key = key[:16].ljust(16, b'0')  # Ensure 16 bytes

    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(input_file, 'rb') as f:
        data = f.read()

    padded_data = pad(data)
    ciphertext = cipher.encrypt(padded_data)

    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext)

def decrypt_file_aes(input_file, output_file, key_str):
    key = key_str.encode('utf-8')
    key = key[:16].ljust(16, b'0')  # Ensure 16 bytes

    with open(input_file, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext))

    with open(output_file, 'wb') as f:
        f.write(decrypted_data)
