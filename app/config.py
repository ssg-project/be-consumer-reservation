import os

# Kafka 설정
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "ticketing-reservation")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "new-reservation-group")

# MySQL 설정
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "enfvh2520!")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "storage_project")
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# Redis 설정
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Websocket 설정
WEBSOCKET_URL = os.getenv("WEBSOCKET_URL", "ws://localhost:8000/ws")
