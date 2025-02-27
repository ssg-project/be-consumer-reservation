from kafka import KafkaConsumer
import json

from app.business_logic import process_reservation
from app.config import KAFKA_BROKER_URL, KAFKA_TOPIC, KAFKA_GROUP_ID
import logging


logger = logging.getLogger(__name__)
# Kafka Consumer 설정
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER_URL,
    group_id=KAFKA_GROUP_ID,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

async def start_consumer():
    """
    Kafka Consumer 시작 및 메시지 처리 루프 실행
    """
    logger.info(f"Starting Kafka Consumer for topic: {KAFKA_TOPIC}")
    
    try:
        for msg in consumer:
            logger.info(f"Received message: {msg.value}")
            await process_reservation(msg.value)
            
    except KeyboardInterrupt:
        logger.info("Consumer stopped manually.")
        
    finally:
        consumer.close()
