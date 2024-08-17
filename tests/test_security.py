from pynethernet.security import generate_hmac, verify_hmac, encrypt_data, decrypt_data


def test_generate_hmac():
    data = b"test data"
    key = b"test key"
    hmac_value = generate_hmac(data, key)
    assert isinstance(hmac_value, str)


def test_verify_hmac():
    data = b"test data"
    key = b"test key"
    hmac_value = generate_hmac(data, key)
    assert verify_hmac(data, hmac_value, key)


def test_encrypt_decrypt_data():
    data = b"test data"
    key = b"thisisaverysecretkeyits32bytes!!"
    encrypted_data = encrypt_data(data, key)
    decrypted_data = decrypt_data(encrypted_data, key)
    assert decrypted_data == data
