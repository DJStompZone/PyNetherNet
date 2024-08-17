import pytest
from unittest.mock import AsyncMock, patch
from pynethernet.websocket_client import connect_to_xbox_live


@pytest.mark.asyncio
async def test_connect_to_xbox_live(mocker):
    # Mock the WebSocket connection
    mock_websocket = AsyncMock()
    mock_websocket.recv.return_value = "mocked STUN/TURN credentials"

    # Patch the websockets.connect method to return our mock_websocket with async context manager support
    with patch("websockets.connect", return_value=mock_websocket) as mock_connect:
        session_id = "test_session_id"
        mctoken = "test_mctoken"

        websocket, connection_info = await connect_to_xbox_live(session_id, mctoken)

        # Assertions
        mock_connect.assert_called_once_with(
            f"wss://signal.franchise.minecraft-services.net/ws/v1.0/signaling/{session_id}",
            extra_headers={
                "Authorization": f"Bearer {mctoken}",
                "Content-Type": "application/json"
            }
        )

        assert websocket == await mock_connect().__aenter__()

