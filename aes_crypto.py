# aes_crypto.py
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii

def encrypt_data(aes_key, plaintext):
    cipher = AES.new(aes_key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext, AES.block_size))
    return binascii.hexlify(cipher.iv).decode(), binascii.hexlify(ct_bytes).decode(), ct_bytes

def decrypt_data(aes_key, iv_hex, ct_hex):
    iv_bytes = binascii.unhexlify(iv_hex)
    ct_bytes = binascii.unhexlify(ct_hex)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv_bytes)
    return unpad(cipher.decrypt(ct_bytes), AES.block_size)
