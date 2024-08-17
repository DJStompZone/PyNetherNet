import hashlib
import hmac
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def generate_hmac(data: bytes, key: bytes) -> str:
    hm = hmac.new(key, data, hashlib.sha256)
    return hm.hexdigest()


def verify_hmac(data: bytes, received_hmac: str, key: bytes) -> bool:
    calculated_hmac = generate_hmac(data, key)
    return hmac.compare_digest(calculated_hmac, received_hmac)


def encrypt_data(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(data, AES.block_size))


def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(encrypted_data), AES.block_size)
