import websockets


async def connect_to_xbox_live(session_id, mctoken):
    url = f"wss://signal.franchise.minecraft-services.net/ws/v1.0/signaling/{session_id}"
    headers = {"Authorization": f"Bearer {mctoken}", "Content-Type": "application/json"}

    async with websockets.connect(url, extra_headers=headers) as websocket:
        # The server sends back STUN/TURN credentials and other connection information.
        connection_info = await websocket.recv()
        print("Received connection info:", connection_info)
        return websocket, connection_info
