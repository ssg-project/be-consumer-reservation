import os
from dotenv import load_dotenv

if not os.getenv("APP_ENV"):
    load_dotenv()

# Kafka 설정
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "127.0.0.1:9093")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "ticketing-reservation")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "new-reservation-group")

# MySQL 설정
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "enfvh2520!")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_NAME = os.getenv("DB_NAME", "ticketing")
# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# Redis 설정
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Websocket 설정
WEBSOCKET_SERVER_URL = os.getenv("WEBSOCKET_SERVER_URL", "ws://127.0.0.1:9000/ws")
