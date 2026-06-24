from aiokafka import AIOKafkaProducer
import json
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

producer = None

async def start_producer():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    await producer.start()

async def stop_producer():
    global producer
    if producer:
        await producer.stop()

async def publish_event(topic: str, event: dict):
    global producer
    await producer.send_and_wait(topic, event)