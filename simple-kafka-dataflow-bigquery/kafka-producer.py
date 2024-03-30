import time
import json
import random
from datetime import datetime
from kafka import KafkaProducer
from faker import Faker

faker = Faker()

config = {}

with open("config.json",'r') as f:
    config = json.loads(f.read())

# Messages will be serialized as JSON
def serializer(message):
    return json.dumps(message).encode("utf-8")


def generate_message():
    return {
        "timestamp": time.time(),
        "latitude": float(faker.latitude()),
        "longitude": float(faker.longitude()),
        "id": faker.pyint(),
    }


# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[config['KAFKA_HOST']],
    value_serializer=serializer
)

if __name__ == "__main__":
    # Infinite loop - runs until you kill the program

    try:
        while True:
            # Generate a message
            dummy_message = generate_message()

            # Send it to our 'messages' topic
            print(
                f"Producing message @ {datetime.now()} | Message = {str(dummy_message)}"
            )
            producer.send(config["KAFKA_TOPIC"], dummy_message)

            # Sleep for a random number of seconds
            time_to_sleep = random.randint(1,5)
            time.sleep(time_to_sleep)
    except KeyboardInterrupt:
        producer.close()
