import pytest
from pynethernet.webrtc_handler import WebRTCHandler


@pytest.mark.asyncio
async def test_webrtc_handler_offer():
    handler = WebRTCHandler()
    offer = await handler.create_offer()
    assert offer is not None


@pytest.mark.asyncio
async def test_webrtc_handler_answer():
    handler = WebRTCHandler()
    offer_sdp = await handler.create_offer()
    answer = await handler.create_answer(offer_sdp)
    assert answer is not None


@pytest.mark.asyncio
async def test_webrtc_handler_ice_candidate():
    handler = WebRTCHandler()
    candidate_sdp = "candidate:0 1 UDP 2122252543 192.168.1.2 12345 typ host"
    await handler.add_ice_candidate(candidate_sdp)
