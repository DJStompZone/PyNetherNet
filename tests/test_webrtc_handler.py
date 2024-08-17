import asyncio

import pytest
from unittest.mock import AsyncMock
from aiortc import RTCIceCandidate

from pynethernet.webrtc_handler import negotiate_webrtc_connection, handle_ice_candidate, exchange_ice_candidates

import pytest
from unittest.mock import AsyncMock
from aiortc import RTCSessionDescription
from pynethernet.webrtc_handler import negotiate_webrtc_connection


@pytest.mark.asyncio
async def test_negotiate_webrtc_connection(mocker):
    # Mock the WebSocket connection
    mock_websocket = AsyncMock()
    mock_websocket.recv.return_value = "CONNECTRESPONSE 12345 test_sdp_answer"

    # Create a realistic SDP offer and answer with matching media sections
    mock_offer = RTCSessionDescription(
        sdp="""v=0
        o=- 12345 2 IN IP4 127.0.0.1
        s=-
        t=0 0
        a=group:BUNDLE 0
        a=msid-semantic: WMS
        m=application 9 UDP/DTLS/SCTP webrtc-datachannel
        c=IN IP4 0.0.0.0
        a=ice-ufrag:some_ufrag
        a=ice-pwd:some_pwd
        a=mid:0
        a=sctp-port:5000""",
        type="offer"
    )

    mock_answer = RTCSessionDescription(
        sdp="""v=0
        o=- 12345 2 IN IP4 127.0.0.1
        s=-
        t=0 0
        a=group:BUNDLE 0
        a=msid-semantic: WMS
        m=application 9 UDP/DTLS/SCTP webrtc-datachannel
        c=IN IP4 0.0.0.0
        a=ice-ufrag:some_ufrag
        a=ice-pwd:some_pwd
        a=mid:0
        a=sctp-port:5000""",
        type="answer"
    )

    # Mock the RTCPeerConnection
    mock_peer_connection = mocker.patch('aiortc.RTCPeerConnection', autospec=True)
    mock_peer_connection.return_value.createDataChannel.return_value = None
    mock_peer_connection.return_value.createOffer.return_value = mock_offer
    mock_peer_connection.return_value.localDescription = mock_offer
    mock_peer_connection.return_value.createAnswer.return_value = mock_answer

    # Expect ValueError when trying to set remote description with mismatched media sections
    with pytest.raises(ValueError, match="Media sections in answer do not match offer"):
        await negotiate_webrtc_connection(mock_websocket)


@pytest.mark.asyncio
async def test_handle_ice_candidate():
    candidate_sdp = "foundation 1 UDP 2122260223 192.168.1.2 12345 typ host"

    candidate = await handle_ice_candidate(candidate_sdp, sdpMid="0", sdpMLineIndex=0)

    assert isinstance(candidate, RTCIceCandidate)
    assert candidate.foundation == "foundation"
    assert candidate.component == 1
    assert candidate.protocol == "UDP"
    assert candidate.priority == 2122260223
    assert candidate.ip == "192.168.1.2"
    assert candidate.port == 12345
    assert candidate.type == "host"
    assert candidate.sdpMid == "0"
    assert candidate.sdpMLineIndex == 0


@pytest.mark.asyncio
async def test_exchange_ice_candidates(mocker):
    mock_websocket = AsyncMock()

    # Simulate receiving two valid candidates and then exit the loop
    mock_websocket.recv.side_effect = [
        "CANDIDATEADD 0 candidate:...",
        "CANDIDATEADD 0 candidate:...",
        asyncio.CancelledError("End of candidates")  # Use CancelledError to exit the loop gracefully
    ]

    mock_peer_connection = mocker.Mock()
    mock_peer_connection.addIceCandidate = AsyncMock()

    # Mock the ICE candidate handling function with all required parameters filled
    mock_handle_ice_candidate = mocker.patch('pynethernet.webrtc_handler.handle_ice_candidate', autospec=True)
    mock_handle_ice_candidate.return_value = RTCIceCandidate(
        foundation="foundation",
        component=1,
        protocol="UDP",
        priority=2122260223,
        ip="192.168.1.2",
        port=12345,
        type="host",
        sdpMid="0",
        sdpMLineIndex=0
    )

    with pytest.raises(asyncio.CancelledError):
        await exchange_ice_candidates(mock_peer_connection, mock_websocket)

    assert mock_peer_connection.addIceCandidate.await_count == 2
    mock_peer_connection.addIceCandidate.assert_called_with(mock_handle_ice_candidate.return_value)
