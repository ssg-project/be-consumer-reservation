from app.config import WEBSOCKET_SERVER_URL
import websockets
import json
import logging

logging.basicConfig(
    filename='debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s'
)

async def ws_send_success(user_id, concert_id):
    data = {
        "type": "reservation_status",
        "user_id": user_id,
        "concert_id": concert_id,
        "status": "success",
    }
    # ws = websocket.create_connection(WEBSOCKET_SERVER_URL)
    await send_to_websocket_server(data)

async def ws_send_fail(user_id, concert_id, msg):
    data = {
        "type": "reservation_status",
        "user_id": user_id,
        "concert_id": concert_id,
        "status": "fail",
        "message": msg
    }
    await send_to_websocket_server(data)

async def send_to_websocket_server(data):
    try:
        async with websockets.connect(WEBSOCKET_SERVER_URL) as ws:
            await ws.send(json.dumps(data))

            print(f"Message sent to WebSocket server: {data}")
            logging.debug(f"Message sent to WebSocket server: {data}")

            response = await ws.recv()
            print(response)
    except Exception as e:
        print(WEBSOCKET_SERVER_URL)
        print(f"Failed to send message to WebSocket server: {e}")
        logging.debug(WEBSOCKET_SERVER_URL)
        logging.debug(f"Failed to send message to WebSocket server: {e}")