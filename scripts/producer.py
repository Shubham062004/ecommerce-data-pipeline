import json
import random
import time
import logging
from datetime import datetime
from kafka import KafkaProducer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def get_producer(broker='localhost:9092'):
    try:
        producer = KafkaProducer(
            bootstrap_servers=[broker],
            value_serializer=json_serializer
        )
        logging.info("Connected to Kafka Producer")
        return producer
    except Exception as e:
        logging.error(f"Error connecting to Kafka: {e}")
        return None

def generate_order():
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami', 'San Francisco']
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'Desk Chair']
    categories = ['Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics', 'Furniture']
    
    product_idx = random.randint(0, len(products)-1)
    
    return {
        'transaction_id': random.randint(10000, 99999),
        'customer_id': f'C{random.randint(100, 999)}',
        'city': random.choice(cities),
        'product_name': products[product_idx],
        'category': categories[product_idx],
        'price': round(random.uniform(10.0, 1500.0), 2),
        'quantity': random.randint(1, 5),
        'transaction_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'completed'
    }

def run_producer():
    topic = 'orders_stream'
    producer = get_producer()
    
    if not producer:
        logging.error("Producer could not be initialized. Exiting.")
        return

    logging.info(f"Starting to stream orders to topic: {topic}")
    
    try:
        while True:
            order = generate_order()
            producer.send(topic, order)
            logging.info(f"Sent order: {order['transaction_id']}")
            time.sleep(random.uniform(1, 3))  # Simulate real-time delay
    except KeyboardInterrupt:
        logging.info("Producer stopped by user")
    finally:
        producer.close()

if __name__ == "__main__":
    run_producer()
