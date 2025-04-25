import psycopg2
from psycopg2 import OperationalError
from config import DB_CONFIG
import logging

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except OperationalError as e:
        logging.error(f"Erro de conexão com o banco: {e}")
        raise

def insert_order(order):
    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO sales (order_number, total, processed_at)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (order_number) DO NOTHING;
                """, (order["order_number"], order["total"], order["processed_at"]))
    except Exception as e:
        logging.error(f"Erro ao inserir pedido {order['order_number']}: {e}")
    finally:
        if conn:
            conn.close()
