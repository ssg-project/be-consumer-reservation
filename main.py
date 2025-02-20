import asyncio
import time
from prometheus_client import start_http_server, Gauge
from app.consumer import start_consumer

if __name__ == '__main__':
    # Prometheus HTTP 서버 시작 (8000 포트)
    start_http_server(8000)
    
    # Kafka Consumer 시작
    asyncio.run(start_consumer())