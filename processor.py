import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from db import insert_order
import logging

def process_message(msg):
    try:
        data = json.loads(msg.value)
        order_number = data["order_number"]
        items = data["order_items"]
        total = sum(item["qty"] * item["value_unit"] for item in items)
        return {
            "order_number": order_number,
            "total": round(total, 2),
            "processed_at": datetime.utcnow()
        }
    except Exception as e:
        logging.error(f"Erro processando mensagem: {e} | Conteúdo: {msg.value()}")
        return None

def process_batch(messages):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(process_message, messages))
        for order in filter(None, results):
            insert_order(order)
