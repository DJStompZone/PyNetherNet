from typing import Dict, Optional, Any

import requests
import os
import json
import binascii
import base64
import struct
import hashlib
import datetime
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding

type PlayfabRequestPayload = dict[str, None | bool | dict[str, bool] | str]


def gen_player_secret():
    """
    Generates a random player secret.

    Returns:
        str: A base64-encoded string representing the player secret.
    """
    return base64.b64encode(os.urandom(32)).decode("UTF-8")


def gen_custom_id():
    """
    Generates a custom ID for the player.

    Returns:
        str: A custom ID string prefixed with 'MCPF' and followed by a hex-encoded random value.
    """
    return "MCPF" + binascii.hexlify(os.urandom(16)).decode("UTF-8").upper()


def import_csp_key(csp):
    """
    Imports a CSP key and returns an RSA public key.

    Args:
        csp (bytes): The CSP key in bytes.

    Returns:
        rsa.RSAPublicKey: The RSA public key derived from the CSP key.
    """
    e = struct.unpack("I", csp[0x10:0x14])[0]
    n = bytearray(csp[0x14:])
    n.reverse()
    n = int(binascii.hexlify(n), 16)
    return rsa.RSAPublicNumbers(e, n).public_key()


def gen_playfab_timestamp():
    """
    Generates a timestamp in ISO 8601 format for PlayFab requests.

    Returns:
        str: The current timestamp in ISO 8601 format with a 'Z' suffix.
    """
    return datetime.datetime.now().isoformat() + "Z"


class PlayFabClient:
    """
    A client for interacting with the PlayFab API.
    """

    TITLE_ID = "20CA2"
    TITLE_SHARED_SECRET = "S8RS53ZEIGMYTYG856U3U19AORWXQXF41J7FT3X9YCWAC7I35X"

    def __init__(self):
        """
        Initializes the PlayFabClient instance, setting up the session and loading settings.
        """
        self.req = None
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "libhttpclient/1.0.0.0",
            "Content-Type": "application/json",
            "Accept-Language": "en-US"
        })
        self.domain = f"https://{self.TITLE_ID.lower()}.playfabapi.com"
        self.settings_file = "settings.json"
        self.playfab_settings = self.load_settings()

    def load_settings(self) -> dict[str, str]:
        """
        Loads settings from a JSON file.

        Returns:
            dict: The settings loaded from the file, or an empty dictionary if the file does not exist.
        """
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        return {}

    def save_settings(self) -> None:
        """
        Saves the current settings to a JSON file.
        """
        with open(self.settings_file, 'w') as f:
            json.dump(self.playfab_settings, f)

    def send_playfab_request(self,
                             endpoint: str,
                             data: PlayfabRequestPayload,
                             headers: Optional[Dict[str, str]] = None
                             ) -> PlayfabRequestPayload:
        """
        Sends a request to the PlayFab API.

        Args:
            endpoint (str): The API endpoint to send the request to.
            data (PlayfabRequestPayload): The payload to send in the request.
            headers (Optional[Dict[str, str]]): Optional headers to include in the request.

        Returns:
            PlayfabRequestPayload: The response data from the API.
        """
        if headers is None:
            headers = {
                "X-PlayFab-Signature": "",
                "X-PlayFab-Timestamp": ""
            }
        try:
            rsp = self.session.post(self.domain + endpoint, json=data, headers=headers)
            rsp.raise_for_status()
            return rsp.json().get('data', {})
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return {}

    def get_mojang_csp(self) -> bytes:
        """
        Retrieves the Mojang CSP public key.

        Returns:
            bytes: The decoded CSP public key.
        """
        return base64.b64decode(self.send_playfab_request("/Client/GetTitlePublicKey", {
            "TitleId": self.TITLE_ID,
            "TitleSharedSecret": self.TITLE_SHARED_SECRET
        })['RSAPublicKey'])

    def gen_playfab_signature(self, request_body: str, timestamp: str) -> bytes:
        """
        Generates a PlayFab signature for a request.

        Args:
            request_body (str): The JSON-encoded request body.
            timestamp (str): The timestamp of the request.

        Returns:
            bytes: The base64-encoded SHA-256 signature.
        """
        sha256 = hashlib.sha256()
        sha256.update(request_body.encode("UTF-8") + b"." + timestamp.encode("UTF-8") + b"." + self.config_get(
            "PLAYER_SECRET").encode("UTF-8"))
        return base64.b64encode(sha256.digest())

    def config_get(self, key: str) -> Any:
        """
        Retrieves a configuration value.

        Args:
            key (str): The key of the configuration value to retrieve.

        Returns:
            Any: The configuration value, or None if the key does not exist.
        """
        return self.playfab_settings.get(key, None)

    def config_set(self, key: str, new_value: Any) -> Any:
        """
        Sets a configuration value and saves the settings.

        Args:
            key (str): The key of the configuration value to set.
            new_value (Any): The new value to set.

        Returns:
            Any: The new value that was set.
        """
        self.playfab_settings[key] = new_value
        self.save_settings()
        return new_value

    def login_with_custom_id(self) -> Optional[Dict[str, Any]]:
        """
        Logs in a user with a custom ID, creating a new account if necessary.

        Returns:
            dict: The response data from the login request.
        """
        custom_id = self.config_get("CUSTOM_ID")
        player_secret = self.config_get("PLAYER_SECRET")
        create_new_account = False

        if custom_id is None:
            custom_id = gen_custom_id()
            create_new_account = True

        if player_secret is None:
            player_secret = gen_player_secret()
            create_new_account = True

        self.config_set("CUSTOM_ID", custom_id)
        self.config_set("PLAYER_SECRET", player_secret)

        payload: PlayfabRequestPayload = {
            "CreateAccount": None,
            "CustomId": None,
            "EncryptedRequest": None,
            "InfoRequestParameters": {
                "GetCharacterInventories": False,
                "GetCharacterList": False,
                "GetPlayerProfile": True,
                "GetPlayerStatistics": False,
                "GetTitleData": False,
                "GetUserAccountInfo": True,
                "GetUserData": False,
                "GetUserInventory": False,
                "GetUserReadOnlyData": False,
                "GetUserVirtualCurrency": False,
                "PlayerStatisticNames": None,
                "ProfileConstraints": None,
                "TitleDataKeys": None,
                "UserDataKeys": None,
                "UserReadOnlyDataKeys": None
            },
            "PlayerSecret": None,
            "TitleId": self.TITLE_ID
        }

        self.req = None
        if create_new_account:
            to_enc = json.dumps({"CustomId": custom_id, "PlayerSecret": player_secret}).encode("UTF-8")
            pubkey = import_csp_key(self.get_mojang_csp())
            payload["CreateAccount"] = True
            payload["EncryptedRequest"] = base64.b64encode(pubkey.encrypt(to_enc, padding.PKCS1v15())).decode("UTF-8")
            self.req = self.send_playfab_request("/Client/LoginWithCustomID", payload)
        else:
            payload["CustomId"] = custom_id
            ts = gen_playfab_timestamp()
            sig = self.gen_playfab_signature(json.dumps(payload), ts)
            self.req = self.send_playfab_request("/Client/LoginWithCustomID", payload, {
                "X-PlayFab-Signature": sig,
                "X-PlayFab-Timestamp": ts
            })
        entity_token = self.req["EntityToken"]["EntityToken"]
        self.session.headers.update({"X-EntityToken": entity_token})
        return self.req
