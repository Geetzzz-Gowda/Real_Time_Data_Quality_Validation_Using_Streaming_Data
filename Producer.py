from kafka import KafkaProducer
import json
import time
import random

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Simulate and send data
def generate_sensor_data():
    return {
        "device_id": f"sensor_{random.randint(1, 5)}",
        "temperature": round(random.uniform(15.0, 40.0), 2),
        "humidity": round(random.uniform(30.0, 90.0), 2),
        "timestamp": time.time()
    }

# Continuously send data
while True:
    data = generate_sensor_data()
    print(f"Sending: {data}")
    producer.send("sensor-data", value=data)
    time.sleep(1)  # 1 second delay
