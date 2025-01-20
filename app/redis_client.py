import redis
from app.config import REDIS_HOST, REDIS_PORT

# Redis 클라이언트 생성
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)