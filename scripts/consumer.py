import json
import logging
import pandas as pd
from kafka import KafkaConsumer
from transform import process_data
from load import load_data
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_consumer(topic, broker='localhost:9092'):
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[broker],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        logging.info(f"Connected to Kafka Consumer for topic: {topic}")
        return consumer
    except Exception as e:
        logging.error(f"Error connecting to Kafka Consumer: {e}")
        return None

def run_consumer():
    topic = 'orders_stream'
    consumer = get_consumer(topic)
    
    if not consumer:
        logging.error("Consumer could not be initialized. Exiting.")
        return

    # Database path
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, 'data', 'ecommerce.db')

    logging.info("Waiting for messages...")
    
    try:
        for message in consumer:
            order_data = message.value
            logging.info(f"Received order: {order_data['transaction_id']}")
            
            # Convert single message to DataFrame for processing
            df = pd.DataFrame([order_data])
            
            # Use existing transformation logic (imputation, features, etc.)
            transformed_df = process_data(df)
            
            # Use existing load logic (idempotent load)
            # Note: In a real streaming app, we might use 'append' for database efficiency,
            # but for this simulation, we'll stick to our production-ready load module.
            load_data(transformed_df, DB_PATH, table_name='transactions_stream')
            
            logging.info(f"Successfully processed and stored order {order_data['transaction_id']}")
            
    except KeyboardInterrupt:
        logging.info("Consumer stopped by user")
    finally:
        consumer.close()

if __name__ == "__main__":
    run_consumer()
