# nethernet/config.py

import os

from dotenv import load_dotenv


def load_config():
    load_dotenv()

    session_id, mctoken, aes_key = check_config()

    return session_id, mctoken, aes_key


def check_config():
    session_id = os.getenv("SESSION_ID")
    mctoken = os.getenv("MCTOKEN")
    aes_key = os.getenv("AES_KEY")

    if not session_id or not mctoken or not aes_key:
        raise ValueError("Missing necessary configuration. Please check your .env file or environment variables.")

    return session_id, mctoken, aes_key
