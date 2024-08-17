import asyncio
import logging
from .websocket_client import WebSocketClient
from .config import SESSION_ID, MCTOKEN


def main():
    """
    The main function that sets up logging and runs the WebSocket client.
    """
    logging.basicConfig(level=logging.INFO)

    async def run_client():
        """
        Asynchronous function to create, connect, and close the WebSocket client.

        Creates an instance of WebSocketClient using SESSION_ID and MCTOKEN,
        connects to the WebSocket server, and then closes the connection.
        """
        client = WebSocketClient(SESSION_ID, MCTOKEN)
        await client.connect()
        await client.close()

    asyncio.run(run_client())


if __name__ == "__main__":
    main()
