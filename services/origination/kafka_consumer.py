from aiokafka import AIOKafkaConsumer
import json
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

async def start_consumer():
    consumer = AIOKafkaConsumer(
        "loan.submitted",
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="origination-group",
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )
    await consumer.start()
    try:
        async for message in consumer:
            print(f"Recieved event: {message.value}")
            print(f"Loan {message.value['loan_id']} submitted for customer {message.value['customer_id']}")
    finally:
        await consumer.stop()