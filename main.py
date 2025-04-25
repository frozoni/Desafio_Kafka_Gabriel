import logging
from kafka_consumer import run_consumer

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        run_consumer()
    except KeyboardInterrupt:
        logging.info("Processo interrompido pelo usuário.")
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
