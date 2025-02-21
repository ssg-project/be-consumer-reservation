from kafka import KafkaConsumer
from prometheus_client import start_http_server, Gauge
import json
import time

from app.business_logic import process_reservation
from app.config import KAFKA_BROKER_URL, KAFKA_TOPIC, KAFKA_GROUP_ID

# Kafka Consumer 설정
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER_URL,
    group_id=KAFKA_GROUP_ID,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Gauge 메트릭 정의
message_processing_time = Gauge('kafka_message_processing_time_seconds', 'Time taken to process a Kafka message in seconds')

async def start_consumer():
    """
    Kafka Consumer 시작 및 메시지 처리 루프 실행
    """
    print(f"Starting Kafka Consumer for topic: {KAFKA_TOPIC}")
    
    try:
        for msg in consumer:
            print(f"Received message: {msg.value}")
            
            # 메시지 처리 시작 시간 기록
            start_time = time.time()
            
            # 메시지 처리 (예: process_reservation 함수 호출)
            await process_reservation(msg.value)
            
            # 메시지 처리 시간 계산
            processing_time = time.time() - start_time
            
            # 처리 시간을 Gauge 메트릭에 기록
            message_processing_time.set(processing_time)
            
            print(f"Message processed in {processing_time:.2f} seconds")
            
    except KeyboardInterrupt:
        print("Consumer stopped manually.")
        
    finally:
        consumer.close()

# 실행
start_consumer()