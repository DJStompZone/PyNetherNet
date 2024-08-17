import asyncio
import logging
from .config import load_config
from .websocket_client import connect_to_xbox_live
from .webrtc_handler import negotiate_webrtc_connection, exchange_ice_candidates

SESSION_ID, MCTOKEN, _ = load_config()


def main():
    """
    The main function that sets up logging and runs the WebSocket client.
    """
    logging.basicConfig(level=logging.INFO)

    async def run_client():
        """
        Asynchronous function to create, connect, and manage WebRTC connection.

        Connects to the Xbox Live WebSocket server, negotiates the WebRTC connection,
        and handles ICE candidates exchange.
        """
        websocket, connection_info = await connect_to_xbox_live(SESSION_ID, MCTOKEN)

        # Set up WebRTC connection
        peer_connection = await negotiate_webrtc_connection(websocket)

        # Exchange ICE candidates
        await exchange_ice_candidates(peer_connection, websocket)

        # Close the WebSocket connection after the WebRTC setup
        await websocket.close()
        await peer_connection.close()

    asyncio.run(run_client())


if __name__ == "__main__":
    main()
