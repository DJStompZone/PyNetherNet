import logging
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate

logger = logging.getLogger(__name__)


class WebRTCHandler:
    """
    Handles WebRTC operations including creating offers, answers, and managing data channels.

    Attributes:
        peer_connection (RTCPeerConnection): The WebRTC peer connection.
        reliable_data_channel (Optional[RTCDataChannel]): The reliable data channel.
        unreliable_data_channel (Optional[RTCDataChannel]): The unreliable data channel.
    """

    def __init__(self):
        """
        Initializes the WebRTCHandler with a new RTCPeerConnection.
        """
        self.peer_connection = RTCPeerConnection()
        self.reliable_data_channel = None
        self.unreliable_data_channel = None

    async def create_offer(self) -> str:
        """
        Creates an SDP offer and sets it as the local description.

        Returns:
            str: The SDP offer as a string.
        """
        offer = await self.peer_connection.createOffer()
        await self.peer_connection.setLocalDescription(offer)
        logger.info("Created SDP offer")
        return self.peer_connection.localDescription.sdp

    async def create_answer(self, offer_sdp: str) -> str:
        """
        Creates an SDP answer in response to an SDP offer and sets it as the local description.

        Args:
            offer_sdp (str): The SDP offer as a string.

        Returns:
            str: The SDP answer as a string.
        """
        offer = RTCSessionDescription(sdp=offer_sdp, type="offer")
        await self.peer_connection.setRemoteDescription(offer)
        answer = await self.peer_connection.createAnswer()
        await self.peer_connection.setLocalDescription(answer)
        logger.info("Created SDP answer")
        return self.peer_connection.localDescription.sdp

    async def add_ice_candidate(self, candidate_sdp: str):
        """
        Adds an ICE candidate to the peer connection.

        Args:
            candidate_sdp (str): The SDP string of the ICE candidate.
        """
        candidate_parts = candidate_sdp.split()
        if len(candidate_parts) < 8:
            logger.error("Invalid ICE candidate format")
            return

        foundation = candidate_parts[0]
        component = int(candidate_parts[1])
        protocol = candidate_parts[2]
        priority = int(candidate_parts[3])
        ip = candidate_parts[4]
        port = int(candidate_parts[5])
        candidate_type = candidate_parts[7]

        related_address = None
        related_port = None
        tcp_type = None

        # Handle optional fields, which may vary depending on the candidate type
        for i in range(8, len(candidate_parts), 2):
            if candidate_parts[i] == "raddr":
                related_address = candidate_parts[i + 1]
            elif candidate_parts[i] == "rport":
                related_port = int(candidate_parts[i + 1])
            elif candidate_parts[i] == "tcptype":
                tcp_type = candidate_parts[i + 1]

        ice_candidate = RTCIceCandidate(
            foundation=foundation,
            component=component,
            protocol=protocol,
            priority=priority,
            ip=ip,
            port=port,
            type=candidate_type,
            relatedAddress=related_address,
            relatedPort=related_port,
            tcpType=tcp_type,
        )

        await self.peer_connection.addIceCandidate(ice_candidate)
        logger.info("Added ICE candidate")

    async def setup_data_channels(self):
        """
        Sets up the data channels for the WebRTC connection.

        Creates two data channels:
        - ReliableDataChannel: An ordered, reliable data channel.
        - UnreliableDataChannel: An unordered, unreliable data channel.
        """
        self.reliable_data_channel = self.peer_connection.createDataChannel("ReliableDataChannel", ordered=True)
        self.unreliable_data_channel = self.peer_connection.createDataChannel("UnreliableDataChannel", ordered=False)
        logger.info("Data channels set up: Reliable and Unreliable")

    async def close(self):
        """
        Closes the WebRTC peer connection.

        This method closes the peer connection and logs the closure.
        """
        await self.peer_connection.close()
        logger.info("WebRTC connection closed")
