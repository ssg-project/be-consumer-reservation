# import asyncio
# import time
# from prometheus_client import start_http_server, Gauge
# from app.consumer import start_consumer

# if __name__ == '__main__':
#     # Prometheus HTTP 서버 시작 (9093 포트)
#     start_http_server(9093)
    
#     # Kafka Consumer 시작
#     asyncio.run(start_consumer())

from app.consumer import start_consumer
import asyncio
import logging



# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - consumer-be - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

if __name__ == '__main__':
    asyncio.run(start_consumer())
