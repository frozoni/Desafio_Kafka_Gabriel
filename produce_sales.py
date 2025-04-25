from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

with open('sales_sample.json', 'r') as f:
    sales = json.load(f)

for sale in sales:
    producer.send('sales', value=sale)
    print(f"Enviado pedido {sale['order_number']}")
    time.sleep(0.1)  # para simular envio em tempo real

producer.flush()
