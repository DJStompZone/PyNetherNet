import pytest
from pynethernet.config import load_config


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("SESSION_ID", "test_session_id")
    monkeypatch.setenv("MCTOKEN", "test_mctoken")
    monkeypatch.setenv("AES_KEY", "test_aes_key")


def test_env_variables(mock_env_vars):
    SESSION_ID, MCTOKEN, AES_KEY = load_config()
    assert SESSION_ID == "test_session_id"
    assert MCTOKEN == "test_mctoken"
    assert AES_KEY == "test_aes_key"

