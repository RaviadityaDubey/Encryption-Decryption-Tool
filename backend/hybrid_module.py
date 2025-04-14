from backend import aes_module, rsa_module
from Crypto.Random import get_random_bytes
import base64

def hybrid_encrypt(message):
    aes_key = get_random_bytes(16)  # 128-bit AES key
    aes_key_b64 = base64.b64encode(aes_key).decode()  # Convert to string
    encrypted_data = aes_module.encrypt_aes(message, aes_key_b64)
    encrypted_key = rsa_module.encrypt_rsa(aes_key_b64)
    return encrypted_key + "::" + encrypted_data

def hybrid_decrypt(combined):
    encrypted_key, encrypted_data = combined.split("::")
    aes_key_b64 = rsa_module.decrypt_rsa(encrypted_key)
    return aes_module.decrypt_aes(encrypted_data, aes_key_b64)
