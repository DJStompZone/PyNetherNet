import json
import logging

import websockets

from .webrtc_handler import WebRTCHandler

logger = logging.getLogger(__name__)


class WebSocketClient:
    """
    A client for handling WebSocket connections and WebRTC negotiations.

    Attributes:
        session_id (str): The session ID for the WebSocket connection.
        token (str): The authorization token for the WebSocket connection.
        url (str): The URL for the WebSocket server.
        websocket (websockets.WebSocketClientProtocol): The WebSocket connection.
        webrtc_handler (WebRTCHandler): The handler for WebRTC operations.
    """

    def __init__(self, session_id: str, token: str):
        """
        Initializes the WebSocketClient with a session ID and token.

        Args:
            session_id (str): The session ID for the WebSocket connection.
            token (str): The authorization token for the WebSocket connection.
        """
        self.session_id = session_id
        self.token = token
        self.url = f"https://signal.franchise.minecraft-services.net/ws/v1.0/signaling/{self.session_id}"
        self.websocket = None
        self.webrtc_handler = WebRTCHandler()

    async def connect(self) -> None:
        """
        Connects to the WebSocket server and receives the initial message.

        Raises:
            websockets.exceptions.InvalidURI: If the URL is invalid.
            websockets.exceptions.InvalidHandshake: If the handshake fails.
        """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.websocket = await websockets.connect(self.url, extra_headers=headers)
        logger.info(f"Connected to WebSocket server at {self.url}")
        await self.receive_initial_message()

    async def receive_initial_message(self) -> None:
        """
        Receives the initial message from the WebSocket server and starts WebRTC negotiation.

        Raises:
            websockets.exceptions.ConnectionClosed: If the connection is closed.
        """
        message = await self.websocket.recv()
        logger.info(f"Received initial message: {message}")
        await self.negotiate_webrtc_connection()

    async def negotiate_webrtc_connection(self) -> None:
        """
        Negotiates the WebRTC connection by sending an SDP offer and handling the response.

        Raises:
            websockets.exceptions.ConnectionClosed: If the connection is closed.
            json.JSONDecodeError: If the response message is not valid JSON.
        """
        sdp_offer = await self.webrtc_handler.create_offer()
        connect_request_message = f"CONNECTREQUEST {self.session_id} {sdp_offer}"
        await self.websocket.send(connect_request_message)
        logger.info("Sent SDP offer")

        response = await self.websocket.recv()
        response_data = json.loads(response)
        if response_data['type'] == 'CONNECTRESPONSE':
            sdp_answer = response_data['sdp']
            await self.webrtc_handler.create_answer(sdp_answer)
            logger.info("Received and set SDP answer")

        for _ in range(3):
            ice_candidate = await self.webrtc_handler.peer_connection.sdp.candidates[0]
            candidate_add_message = f"CANDIDATEADD {self.session_id} {ice_candidate}"
            await self.websocket.send(candidate_add_message)
            logger.info("Sent ICE candidate")

        remote_candidate_message = await self.websocket.recv()
        remote_candidate = json.loads(remote_candidate_message)['candidate']
        await self.webrtc_handler.add_ice_candidate(remote_candidate)
        logger.info("Added remote ICE candidate")

        await self.webrtc_handler.setup_data_channels()

    async def close(self) -> None:
        """
        Closes the WebSocket and WebRTC connections.

        Raises:
            websockets.exceptions.ConnectionClosed: If the connection is already closed.
        """
        await self.webrtc_handler.close()
        await self.websocket.close()
        logger.info("WebSocket and WebRTC connection closed")
