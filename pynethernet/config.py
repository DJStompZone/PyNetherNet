import os
from dotenv import load_dotenv

load_dotenv()

SESSION_ID = os.getenv("SESSION_ID")
MCTOKEN = os.getenv("MCTOKEN")
AES_KEY = os.getenv("AES_KEY")

if not SESSION_ID or not MCTOKEN or not AES_KEY:
    raise ValueError("Missing necessary configuration. Please check your .env file or environment variables.")
