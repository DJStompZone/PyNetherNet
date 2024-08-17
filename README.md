# PyNetherNet

`pynethernet` is a Python library that provides an API allowing users to interact with Minecraft: Bedrock Edition realms and servers via the NetherNet WebRTC protocol.

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