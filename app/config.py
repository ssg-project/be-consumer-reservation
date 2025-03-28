import os
from dotenv import load_dotenv
import boto3
import json
from botocore.exceptions import ClientError

if not os.getenv("APP_ENV"):
    load_dotenv()

    # Kafka 설정
    KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
    KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID")

    # MySQL 설정
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")

    # Redis 설정
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT"))

    # Websocket 설정
    WEBSOCKET_SERVER_URL = os.getenv("WEBSOCKET_SERVER_URL")

else:
    secret_name = "secret/ticketing/reserve"
    region_name = "ap-northeast-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    
    secret_data = json.loads(secret)

    REDIS_HOST = secret_data["REDIS_HOST"]
    REDIS_PORT = secret_data["REDIS_PORT"]

    KAFKA_BROKER_URL = secret_data["KAFKA_BROKER_URL"]
    KAFKA_TOPIC = secret_data["KAFKA_TOPIC"]
    KAFKA_GROUP_ID = secret_data["KAFKA_GROUP_ID"]

    WEBSOCKET_SERVER_URL = secret_data["WEBSOCKET_SERVER_URL"]


    db_secret_name = "secret/ticketing/rds"

    try:
        db_secret_response = client.get_secret_value(
            SecretId=db_secret_name
        )
    except ClientError as e:
        raise e
    
    db_secret = db_secret_response['SecretString']
    db_secret_data = json.loads(db_secret)
    
    # DB 관련 정보 설정
    DB_USER = db_secret_data["username"]
    DB_PASS = db_secret_data["password"]
    DB_HOST = db_secret_data["host"]
    DB_PORT = db_secret_data["port"]
    DB_NAME = db_secret_data["dbInstanceIdentifier"]