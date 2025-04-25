Desafio Técnico: Processamento Paralelo de Vendas em Tempo Real

Visão Geral

Este projeto tem como objetivo consumir mensagens em tempo real do Apache Kafka contendo pedidos de vendas, processá-los em lotes de 100 mensagens com paralelismo, e armazenar o valor total de cada pedido em um banco de dados relacional PostgreSQL.

Tecnologias Utilizadas

Python 3.8+

Apache Kafka

PostgreSQL

Docker & Docker Compose

kafka-python

psycopg2

Estrutura do Projeto

.
├── config.py               # Configuração do DB
├── db.py                   # Conexão e inserção no banco
├── kafka_consumer.py       # Consumo de mensagens Kafka
├── processor.py            # Processamento paralelo e agregação
├── main.py                 # Ponto de entrada da aplicação
├── sales_sample.json       # Exemplo com 100 pedidos
├── docker-compose.yml      # Ambiente completo via Docker
├── requirements.txt        # Dependências Python
└── README.md               # Este arquivo

Instalação e Execução

1. Clonar o repositório

git clone https://github.com/frozoni/desafio-kafka-vendas.git
cd desafio-kafka-vendas

2. Subir os containers com Kafka e PostgreSQL

docker compose up -d

3. Criar ambiente virtual e instalar dependências

python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt

4. Executar o consumidor Kafka

python main.py

5. Enviar mensagens de exemplo (opcional)

python produce_sales.py

Banco de Dados

A aplicação salva os dados em uma tabela chamada sales com a seguinte estrutura:

CREATE TABLE sales (
    order_number INT PRIMARY KEY,
    total NUMERIC,
    processed_at TIMESTAMP
);

Variáveis de Ambiente (config.py)

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "postgres",
    "dbname": "salesdb"
}

Abordagem de Paralelismo

O processamento paralelo é feito com ThreadPoolExecutor, que permite paralelizar a execução de cada mensagem dentro do lote de 100:

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(process_message, messages))

Essa abordagem permite ganho de desempenho ao utilizar múltiplas threads para processar mensagens simultaneamente, especialmente útil quando o cálculo do total do pedido é custoso.

Tratamento de Erros

Mensagens malformadas: ignoradas com logging.

Falha no banco: tratada com try/except e log do erro. A execução é pausada se o banco estiver inacessível.

Testes e Validação

Após o processamento, execute:

SELECT * FROM sales ORDER BY order_number;

Autor

Gabriel Frozoni

jfrozoni@gmail.com

