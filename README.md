# PyNetherNet

`pynethernet` is a Python library that provides an API allowing users to interact with Minecraft: Bedrock Edition realms and servers via the NetherNet WebRTC protocol.

[![Tests Badge](https://github.com/DJStompZone/PyNetherNet/actions/workflows/run-tests.yml/badge.svg)](https://github.com/DJStompZone/PyNetherNet/actions/workflows/run-tests.yml) ![](https://img.shields.io/badge/Python_Version-_3.12+-55cc00?labelColor=333333&logo=python) ![](https://img.shields.io/badge/Protocol_Version-%20712+-4400cc?labelColor=333333&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1NDYiIGhlaWdodD0iNjUxIj48cGF0aCBkPSJtMS41OCAxNTkgMjcyIDgyLjZ2NDA4bC0yNzItMTIweiIgZmlsbD0iIzViNDIyZCIvPjxwYXRoIGQ9Ik0xLjUgMTk4bDE3IDcuNVYxODBsMTcgNy41VjIxM2wzNCAxNS0uMDA3IDI1LjUgMTcgNy41LS4wMDctNzYuNSAxNyA3LjQ4LS4wMyA1MSAxNyA3LjUuMDAzLTI1LjUgMTcgNy41LjAxMiA1MSAxNyA3LjUuMDctMjUuNSAxNi45IDcuNDh2MjUuNWwxNyA3LjV2LTI1LjVsMTcgNy41Mi0uMDEtMjUuNSAxNyA3LjUtLjAwOCAyNS41IDM0IDE1LS4wMS0yNS41IDE3IDcuNXYtNTFsLTI3Mi0xMjB6IiBmaWxsPSIjNjRhNDNhIiBzdHJva2U9IiM2NGE0M2EiLz48cGF0aCBkPSJNMS43IDEyMWwyNzIgMTIwIDI3MS0xMjAtMjcyLTEyMHoiIGZpbGw9IiM1YTlhMzAiIHN0cm9rZT0iIzVhOWEzMCIvPjxwYXRoIGQ9Im01NDUgMTcyLTI3MiA2OS4ydjQwOGwyNzItMTIweiIgZmlsbD0iIzRmMzYyNCIgc3Ryb2tlPSIjNGYzNjI0Ii8+PHBhdGggZD0iTTU0NSAxMjJsLjE1NCA1MC45LTE3IDcuNS4wNzMgMjUuNS0zNCAxNS0uMDczLTI1LjUtMTYuOSA3LjQ3LjAwMyAyNS41LTE3IDcuNS0uMDAzIDI1LjUtMTcgNy41LS4wMDMtMjUuNS0xNyA3LjUtLjIgMjUuNi0xNi44IDcuNDIuMDAzLTUxLTE3IDcuNTQuMDA4IDI1LjUtMTYuMyA3LjItLjY1NS01MC43LTE3IDcuNS0uMDA3IDc2LjUtMTcgNy41di0yNS41bC0zNCAxNXYtMjUuNWwtMTcgNy41djI1LjVsLTE3IDcuNS0uMDA0LTc2LjV6IiBmaWxsPSIjM2I2MTIxIiBzdHJva2U9IiMzYjYxMjEiLz48L3N2Zz4=)

## Features

- Connect to Xbox Live WebSocket server
- Negotiate WebRTC connections
- Handle ICE candidates exchange
- Encrypt and decrypt data using AES
- Generate and verify HMACs
- Interact with the PlayFab API

## Requirements

- Python 3.12 or higher

## Installation

You can install `pynethernet` via `pip`:
```sh
pip install git+https://github.com/DJStompZone/pynethernet.git

# or

git clone https://github.com/DJStompZone/pynethernet.git
cd pynethernet
pip install .
```

## Usage

### Configuration

Create a `.env` file in the root directory of your project and add the following environment variables:

```
SESSION_ID=your_session_id
MCTOKEN=your_mctoken
AES_KEY=your_aes_key
```

### Running the Main Script

To run the main script, execute:

```sh
python -m pynethernet
```

### Example Code

#### Connecting to Xbox Live and Negotiating WebRTC Connection

```python
import asyncio, os

import dotenv
from pynethernet.websocket_client import connect_to_xbox_live
from pynethernet.webrtc_handler import negotiate_webrtc_connection, exchange_ice_candidates

dotenv.load_dotenv()

SESSION_ID = os.getenv("SESSION_ID")
MCTOKEN = os.getenv("MCTOKEN")

async def main():
    websocket, connection_info = await connect_to_xbox_live(SESSION_ID, MCTOKEN)
    peer_connection = await negotiate_webrtc_connection(websocket)
    await exchange_ice_candidates(peer_connection, websocket)
    await websocket.close()
    await peer_connection.close()

asyncio.run(main())
```

## Work in Progress ⚠️

This project is still a work in progress and is currently very early in development.
The API is subject to change and the code is not yet stable. See below for instructions on how to contribute.

## Contributing

Contributions are welcome! Please open an [issue](https://github.com/DJStompZone/PyNetherNet/issues) or submit a [pull request](https://github.com/DJStompZone/PyNetherNet/pulls) on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/DJStompZone/PyNetherNet/blob/main/LICENSE) file for details.

## Authors

- DJ Stomp \<85457381+DJStompZone@users.noreply.github.com\>
