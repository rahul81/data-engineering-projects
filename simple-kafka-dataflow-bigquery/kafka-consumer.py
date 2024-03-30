import json 
from kafka import KafkaConsumer


config = {}

with open("config.json",'r') as f:
    config = json.loads(f.read())

if __name__ == '__main__':
    # Kafka Consumer 
    consumer = KafkaConsumer(
        config['KAFKA_TOPIC'],
        bootstrap_servers=config['KAFKA_HOST'],  
        auto_offset_reset='earliest',
        enable_auto_commit=True,
    )

    try:

        for message in consumer:
            print("Consumed message >> ", json.loads(message.value))

    except KeyboardInterrupt:
        consumer.close()