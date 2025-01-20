from websocket import create_connection
from app.config import WEBSOCKET_URL
import json

ws = create_connection(WEBSOCKET_URL)

def ws_send_success(user_id, concert_id):
    return ws.send(
            json.dumps({
                "type": "reservation_status",
                "user_id": user_id,
                "concert_id": concert_id,
                "status": "success",
            }))

def ws_send_fail(user_id, concert_id, msg):
    return ws.send(
            json.dumps({
                "type": "reservation_status",
                "user_id": user_id,
                "concert_id": concert_id,
                "status": "fail",
                "message": msg
            }))
