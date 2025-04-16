from confluent_kafka import Consumer
import requests
from web3 import Web3

# Kafka Consumer Configuration
kafka_config = {
    'bootstrap.servers': 'kafka:9092',  # Kafka hostname in the Docker network
    'group.id': 'crypto-log-consumer',
    'auto.offset.reset': 'earliest'  # Start from the earliest message
}
consumer = Consumer(kafka_config)
topic = 'crypto_transactions'
consumer.subscribe([topic])

# Connect to an Ethereum node (e.g., Alchemy, Infura, etc.)
w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/your_key_here'))

# Gas threshold for classification
GAS_THRESHOLD = 21000  # Example threshold for high gas usage

# Function to decode transaction details and classify gas usage
def process_transaction(tx_hash):
    try:
        # Fetch transaction details using the hash
        tx = w3.eth.get_transaction(tx_hash)
        
        # Extract the gas value
        gas = tx.get('gas', 0)  # Default to 0 if gas is missing
        
        # Classify the transaction based on gas
        classification = "HIGH" if gas > GAS_THRESHOLD else "LOW"

        # Log the processed transaction
        print({
            "tx_hash": tx_hash,
            "from": tx['from'],
            "to": tx['to'],
            "gas": gas,
            "classification": classification
        })
    except Exception as e:
        print(f"Error processing transaction {tx_hash}: {e}")

print(f"Listening to Kafka topic: {topic}")
try:
    while True:
        message = consumer.poll(1.0)  # Poll for new messages
        if message is None:
            continue
        if message.error():
            print(f"Error: {message.error()}")
            continue

        # Decode the transaction hash
        tx_hash = message.value().decode('utf-8')
        print(f"Processing transaction: {tx_hash}")

        # Process the transaction and classify gas usage
        process_transaction(tx_hash)

except KeyboardInterrupt:
    print("Stopped by user")
finally:
    consumer.close()