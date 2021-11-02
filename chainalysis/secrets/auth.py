import shrimpy
from cryptography.fernet import Fernet

def get_client():
    public_key="ea62910b320683b516c1b5992d73e3de985df3c36086c2349c29d55c392d3a6b"
    secret_key=decrypt_secret("secrets/enc_key.txt", "secrets/symkey.key")
    return shrimpy.ShrimpyApiClient(public_key, secret_key)

def decrypt_secret(secret_path, key_path):
    with open(key_path, 'rb') as key_buffer:
        key = key_buffer.read()
    with open(secret_path, 'rb') as secret_buffer:
        secret = secret_buffer.read()
    f = Fernet(key)
    return f.decrypt(secret)

