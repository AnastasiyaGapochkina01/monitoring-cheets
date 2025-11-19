from kafka import KafkaConsumer
import psycopg2
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import json
import time

consumer = KafkaConsumer(
    'numbers',
    bootstrap_servers='kafka:9092',
    group_id='worker-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

conn = None
cursor = None
processed_total = 0

def push_metrics(count):
    registry = CollectorRegistry()
    g = Gauge('worker_processed_messages_total', 'Total messages processed by worker', registry=registry)
    g.set(count)
    push_to_gateway('pushgateway:9091', job='batch_worker', registry=registry)

def create_table():
    global cursor, conn
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processed_counts (
        id SERIAL PRIMARY KEY,
        count INTEGER NOT NULL,
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()

def process_batch():
    global processed_total
    batch_size = 5
    batch = []
    for message in consumer:
        batch.append(message.value)
        if len(batch) >= batch_size:
            count = len(batch)
            processed_total += count
            cursor.execute("INSERT INTO processed_counts (count) VALUES (%s)", (count,))
            conn.commit()
            print(f"Processed batch of {count} messages.")
            push_metrics(processed_total)
            batch.clear()
        time.sleep(1)

if __name__ == '__main__':
    conn = psycopg2.connect(dbname='metricsdb', user='user', password='password', host='postgres')
    cursor = conn.cursor()
    create_table()
    process_batch()
