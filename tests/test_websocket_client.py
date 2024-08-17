import pytest
from pynethernet.websocket_client import WebSocketClient
from pynethernet.config import SESSION_ID, MCTOKEN


@pytest.mark.asyncio
async def test_websocket_client_init():
    client = WebSocketClient(SESSION_ID, MCTOKEN)
    assert client.session_id == SESSION_ID
    assert client.token == MCTOKEN
    assert client.url == f"https://signal.franchise.minecraft-services.net/ws/v1.0/signaling/{SESSION_ID}"


@pytest.mark.asyncio
async def test_websocket_client_connect(mocker):
    client = WebSocketClient(SESSION_ID, MCTOKEN)
    mocker.patch('websockets.connect', return_value=mocker.AsyncMock())
    await client.connect()
    assert client.websocket is not None
