from kafka import KafkaProducer
import time
import json

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def produce_messages():
    i = 0
    while True:
        msg = {'number': i}
        producer.send('numbers', value=msg)
        print(f"Produced: {msg}")
        i += 1
        time.sleep(2)

if __name__ == '__main__':
    produce_messages()
