import time
import requests
from confluent_kafka import Producer

# Configuration for Kafka Producer
kafka_config = {
    'bootstrap.servers': 'kafka:9092',
    'client.id': 'crypto-transaction-producer'
}
producer = Producer(kafka_config)
topic = 'crypto_transactions'

# Function to fetch data from Alchemy API
def fetch_transactions_from_alchemy():
    alchemy_api_url = 'https://eth-mainnet.alchemyapi.io/v2/your_alchemy_api_key_here'
    params = {
        'method': 'alchemy_getAssetTransfers',
        'params': [
            {
                "fromBlock": "latest",
                "toBlock": "latest",
                "category": ["external", "internal"]
            }
        ],
        'jsonrpc': '2.0',
        'id': 1
    }
    response = requests.post(alchemy_api_url, json=params)
    if response.status_code == 200:
        return response.json().get('result', {}).get('transfers', [])
    else:
        print(f"Error fetching data from Alchemy: {response.text}")
        return []

# Function to produce messages to Kafka
# def produce_to_kafka(transactions):
#     for transaction in transactions:
#         producer.produce(topic, key=transaction['hash'], value=str(transaction))
#         print(f"Produced transaction: {transaction['hash']}")

def produce_to_kafka(transactions):
    for transaction in transactions:
        tx_hash = transaction['hash']  # Extract only the hash
        producer.produce(topic, key=tx_hash, value=tx_hash)
        print(f"Produced transaction: {tx_hash}")

# Main loop to fetch and produce data
while True:
    transactions = fetch_transactions_from_alchemy()
    if transactions:
        produce_to_kafka(transactions)
    producer.flush()
    time.sleep(10)  # Fetch new data every 10 seconds