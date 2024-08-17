from typing import Optional
import logging

from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate

logger = logging.getLogger(__name__)


async def negotiate_webrtc_connection(websocket):
    peer_connection = RTCPeerConnection()
    _ = peer_connection.createDataChannel("chat")

    offer = await peer_connection.createOffer()
    await peer_connection.setLocalDescription(offer)

    connect_request = f"CONNECTREQUEST {peer_connection.localDescription.sdp}"
    await websocket.send(connect_request)

    response = await websocket.recv()
    sdp_answer = response.split(" ", 2)[2]
    answer = RTCSessionDescription(sdp=sdp_answer, type="answer")
    await peer_connection.setRemoteDescription(answer)

    await exchange_ice_candidates(peer_connection, websocket)

    return peer_connection


async def handle_ice_candidate(candidate_sdp: str, sdpMid: Optional[str] = None,
                               sdpMLineIndex: Optional[int] = None) -> RTCIceCandidate:
    """
        Adds an ICE candidate to the peer connection.

        Args:
            candidate_sdp (str): The SDP string of the ICE candidate.
            sdpMid (str, optional): The media stream identification. Defaults to None.
            sdpMLineIndex (int, optional): The media line index. Defaults to None.
        """
    candidate_parts = candidate_sdp.split()
    if len(candidate_parts) < 8:
        logger.error("Invalid ICE candidate format")
        raise ValueError("Invalid ICE candidate format")

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
        sdpMid=sdpMid,
        sdpMLineIndex=sdpMLineIndex
    )

    return ice_candidate


async def exchange_ice_candidates(peer_connection, websocket):
    @peer_connection.on("icecandidate")
    async def on_ice_candidate(_candidate):

        if _candidate:
            candidate_message = f"CANDIDATEADD {peer_connection.localDescription.sdpMid} {_candidate.sdp}"
            await websocket.send(candidate_message)

    while True:
        candidate_msg = await websocket.recv()
        if candidate_msg.startswith("CANDIDATEADD"):
            _, sdp_mid, candidate_sdp = candidate_msg.split(" ", 2)
            __candidate = await handle_ice_candidate(candidate_sdp, sdpMid=sdp_mid)
            await peer_connection.addIceCandidate(__candidate)
