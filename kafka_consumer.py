from kafka import KafkaConsumer
from processor import process_batch
import logging

def run_consumer():
    consumer = KafkaConsumer(
        'sales',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='sales-group',
        value_deserializer=lambda x: x.decode('utf-8')
    )

    buffer = []

    for msg in consumer:
        buffer.append(msg)
        if len(buffer) >= 100:
            process_batch(buffer)
            buffer.clear()
