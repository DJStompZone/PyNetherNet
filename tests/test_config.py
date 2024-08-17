from pynethernet.config import SESSION_ID, MCTOKEN, AES_KEY


def test_env_variables():
    assert SESSION_ID is not None, "SESSION_ID is not set"
    assert MCTOKEN is not None, "MCTOKEN is not set"
    assert AES_KEY is not None, "AES_KEY is not set"
