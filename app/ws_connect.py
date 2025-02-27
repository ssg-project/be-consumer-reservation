from app.config import WEBSOCKET_SERVER_URL
import websockets
import json
import logging

logger = logging.getLogger(__name__)

async def ws_send_success(user_id, concert_id):
    data = {
        "type": "reservation_status",
        "user_id": user_id,
        "concert_id": concert_id,
        "status": "success",
    }
    logger.info("ws_send_success")
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
    logger.info("ws_send_fail")
    await send_to_websocket_server(data)

async def send_to_websocket_server(data):
    try:
        async with websockets.connect(WEBSOCKET_SERVER_URL) as ws:
            await ws.send(json.dumps(data))

            logger.info(f"Message sent to WebSocket server: {data}")

            response = await ws.recv()
            print(response)
            logger.info(f"response: {response}")
    except Exception as e:
        logger.info(WEBSOCKET_SERVER_URL)
        logger.info(f"Failed to send message to WebSocket server: {e}")