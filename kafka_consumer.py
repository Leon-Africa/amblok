import time
import psycopg2
from psycopg2 import OperationalError
from confluent_kafka import Consumer
from web3 import Web3

# Function to connect to PostgreSQL with retries
def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname="transactions",
                user="user",
                password="password",
                host="postgres",
                port="5432"
            )
            return conn
        except OperationalError:
            print("Database not ready, retrying in 5 seconds...")
            time.sleep(5)

# Establish database connection
conn = connect_to_db()
cursor = conn.cursor()

# Create Table (if not exists)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS TransactionAnalysis (
        tx_hash VARCHAR PRIMARY KEY,
        wallet_from VARCHAR,
        wallet_to VARCHAR,
        gas INTEGER,
        classification VARCHAR
    )
""")
conn.commit()

# Kafka Consumer Configuration
kafka_config = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'crypto-log-consumer',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(kafka_config)
topic = 'crypto_transactions'
consumer.subscribe([topic])

# Ethereum Configuration
w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/your_key_here'))
GAS_THRESHOLD = 21000

# Function to decode transaction details and classify gas usage
def process_transaction(tx_hash):
    global conn, cursor
    try:
        # Reconnect to the database if the connection is lost
        if conn.closed != 0:
            print("Database connection lost. Reconnecting...")
            conn = connect_to_db()
            cursor = conn.cursor()

        # Fetch transaction details using the hash
        tx = w3.eth.get_transaction(tx_hash)
        gas = tx.get('gas', 0)
        classification = "HIGH" if gas > GAS_THRESHOLD else "LOW"

        # Insert the processed data into PostgreSQL
        cursor.execute("""
            INSERT INTO TransactionAnalysis (tx_hash, wallet_from, wallet_to, gas, classification)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (tx_hash) DO NOTHING
        """, (tx_hash, tx['from'], tx['to'], gas, classification))
        conn.commit()

        print(f"Stored transaction: {tx_hash}")
    except Exception as e:
        print(f"Error processing transaction {tx_hash}: {e}")

# Poll for Kafka messages and process transactions
print(f"Listening to Kafka topic: {topic}")
try:
    while True:
        message = consumer.poll(1.0)  # Poll Kafka for new messages
        if message is None:
            continue
        if message.error():
            print(f"Error: {message.error()}")
            continue

        # Decode and validate the transaction hash
        try:
            # Decode transaction hash from the Kafka message
            tx_hash = message.value().decode('utf-8')

            # Validate that tx_hash is a proper Ethereum transaction hash
            if not tx_hash.startswith('0x') or len(tx_hash) != 66:
                raise ValueError(f"Invalid transaction hash: {tx_hash}")

            print(f"Processing transaction: {tx_hash}")
            process_transaction(tx_hash)  # Process the validated transaction hash
        except Exception as e:
            print(f"Error decoding or validating transaction message: {e}")

except KeyboardInterrupt:
    print("Stopped by user")
finally:
    consumer.close()
    cursor.close()
    conn.close()