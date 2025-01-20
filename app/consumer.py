from kafka import KafkaConsumer
import json

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

def start_consumer():
    """
    Kafka Consumer 시작 및 메시지 처리 루프 실행
    """
    print(f"Starting Kafka Consumer for topic: {KAFKA_TOPIC}")
    
    try:
        for msg in consumer:
            print(f"Received message: {msg.value}")
            process_reservation(msg.value)  # 비즈니스 로직 호출
            
    except KeyboardInterrupt:
        print("Consumer stopped manually.")
        
    finally:
        consumer.close()
