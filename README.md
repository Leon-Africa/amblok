# amblok 

This project is a blockchain transaction processor system that consists of a Kafka producer and consumer. The producer fetches Ethereum transaction data from the Alchemy API and sends it to a Kafka topic. The consumer reads transaction hashes from the topic, fetches transaction details using Web3, and stores the processed information in a PostgreSQL database. Hence effectively a modern blockchain transactions processor to which you can hook up your AI/ML - add more logic - have fun with it!

## Prerequisites

Before running the project, ensure you have the following installed on your system:
- Docker
- A valid Alchemy API key for interacting with the Ethereum blockchain

## Project Structure

- **`producer.py`**: The Kafka producer that fetches Ethereum transactions and sends them to a Kafka topic.
- **`consumer.py`**: The Kafka consumer that processes transaction hashes and stores the details in a PostgreSQL database.
- **`docker-compose.yml`**: The configuration file for setting up the services using Docker Compose.
- **`PostgreSQL Database`**: Used to store processed transaction data.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Leon-Africa/amblok.git
cd amblok
```

Replace `your_alchemy_api_key_here` Alchemy API key in [kafka_producer.py](https://github.com/Leon-Africa/amblok/blob/38994b50ebc0b28fc7ef59df7f7d5b11d880ecfe/kafka_producer.py#L15) and [kafka_consumer.py](https://github.com/Leon-Africa/amblok/blob/38994b50ebc0b28fc7ef59df7f7d5b11d880ecfe/kafka_consumer.py#L50)

### 2. Build and Start the Services
Use Docker Compose to build and start the services:
```bash
docker compose up --build --no-cache
```

This command will start the following services:
- **Kafka**: A distributed messaging system.
- **Zookeeper**: Required by Kafka for managing configurations.
- **Producer**: Fetches transactions and produces messages to Kafka.
- **Consumer**: Consumes messages from Kafka and writes transaction data to PostgreSQL.
- **PostgreSQL**: The database for storing transaction analysis.

### 4. Verify the Services
- Check the logs for the producer:
  ```bash
  docker compose logs -f producer
  ```
  You should see logs like:
  ```
  Produced transaction: 0x7d20a691a4793be6e2bbd5cc2c3be5a3b73ff59125aa3008efa6dbd926ad9004
  ```

- Check the logs for the consumer:
  ```bash
  docker compose logs -f consumer
  ```
  You should see logs like:
  ```
  Stored transaction: 0x7d20a691a4793be6e2bbd5cc2c3be5a3b73ff59125aa3008efa6dbd926ad9004
  ```

### 5. Access the PostgreSQL Database
To verify if data is being written to the PostgreSQL database:
1. Access the running PostgreSQL container:
   ```bash
   docker exec -it amblok-postgres-1 psql -U user -d transactions
   ```
2. Query the `transactionanalysis` table:
   ```sql
   SELECT * FROM transactionanalysis;
   ```

### Transaction Analysis Table

Below is a table representing the transaction analysis data:

| tx_hash                                                       | wallet_from                                   | wallet_to                                     | gas     | classification |
|---------------------------------------------------------------|-----------------------------------------------|-----------------------------------------------|---------|----------------|
| 0xf02d913cfa66f17d3ef2dc046ade54dc3e533d58f583d6cceaa70bd62c1c1e5d | 0xD1Fa51f2dB23A9FA9d7bb8437b89FB2E70c60cB7    | 0xd4bC53434C5e12cb41381A556c3c47e1a86e80E3    | 1149548 | HIGH           |
| 0xaaa4e2ec602dc630a7c90150fb336929a89d04309898ab45788e903333ee9943 | 0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13    | 0x1f2F10D1C40777AE1Da742455c65828FF36Df387    | 1125820 | HIGH           |
| 0xf806d0364a34c689b905d8f5ead1bab8426c5f095056c18060cb29b8ac7c6d38 | 0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13    | 0x1f2F10D1C40777AE1Da742455c65828FF36Df387    |  680617 | HIGH           |
| 0x08561d25e715731d0d505d45495f48ba968548994d930c03db0aa3d642518422 | 0xf89d7b9c864f589bbF53a82105107622B35EaA40    | 0x290a07aC2d2fdC222e43356B6217b94f8Bf7512A    |   90000 | HIGH           |
| 0x337fda2921ab9fed6183c95b547ad350c451dc098edf7a275881ea5462735e1a | 0xf89d7b9c864f589bbF53a82105107622B35EaA40    | 0x8Eb2d2a5eD947a36c4D9A1363234044bD88b09B3    |   90000 | HIGH           |
| 0xb858f7b01474ecd575e2a44d09ca04084416a8147510aa929bb8e9fb9cece22a | 0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549    | 0xebB6Cb2926c816314b422a907FbaDEcbA3a3d5bf    |  207128 | HIGH           |
| 0xe03ed5d41a96eec0dda994c9dbe8f2672434cf64792cf7d95acd352ad185b98f | 0x429aC89e7Eb25acEaD448F0c4Cd7ee2018f53e05    | 0xF96Ab834f25ee7B03dD7075078B05582C47156d2    |   21000 | LOW            |
| 0x9006e6ae966df93576cbea29130071944cc6993f713b57f3972b4438ff64a51a | 0x6046945C5B5eF5933b8E73a98A6AD7bF3e031df7    | 0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C    |  706738 | HIGH           |
| 0xf6690c2a2008817fb79ccbd722b456039e382aa8ec8d0f6eb94c0b52f1a71632 | 0x6046945C5B5eF5933b8E73a98A6AD7bF3e031df7    | 0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C    |  393768 | HIGH           |
| 0xc242b31f5142ecde7013c7e6f3941c8a925c211af6a92966d08beb9d00199725 | 0x00000027F490ACeE7F11ab5fdD47209d6422C5a7    | 0x42E213a3ad048e899B89ea8CB11d21bc97b84748    |  244825 | HIGH           |
| 0x29f12106d1b871ce947f19c0279335785a1c0606cb990c64e7c6a0ffc5fd420c | 0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5    | 0xeDa4C0F725466fF036B03B2AD532904d6A96473E    |   21000 | LOW            |         |
| 0x5c4fd16df98374ed34717bb904183bd235f4c5da5768aa6ed68f6ed0a5f62a95 | 0x0e39140A8B1683e7ED0e737994846A47D9801Cdd    | 0x69460570c93f9DE5E2edbC3052bf10125f0Ca22d    |  215497 | HIGH           |
| 0xef167ca262fb0981479249167cb7f7b51039ffd23f318f39e86420b496527308 | 0xa4B5B81041E342A37373FFae4e170e4f5761B3e4    | 0x69460570c93f9DE5E2edbC3052bf10125f0Ca22d    |  154527 | HIGH           |
| 0x72b47db5a2de8cdc67b562343cb0b87a09cf9ddef8f6056009bedd563f652dd8 | 0xA14Bf4Cbe15ddf33537a0e50dEC1BA34769FFd29    | 0xfB183eb452CEe258c7e429610cb7d9e2a5fA68Ff    |   21000 | LOW            |
| 0xf6c363a1b340cb5547c708dd3da5dc77121b797cdf5fe59bcc481d84595d8265 | 0xb9134ddEB7Db85F9742659a8F74bE87328F138D1    | 0x0aBbc482FBD91DBF413E3D6Cc5622e03552AC13a    |   21000 | LOW            |


### 6. Stop the Services
To stop all running services cleanly:
```bash
docker compose down
```

## Project Workflow

1. **Producer**:
   - Fetches Ethereum transactions from the Alchemy API.
   - Sends transaction hashes to the Kafka topic `crypto_transactions`.

2. **Consumer**:
   - Reads transaction hashes from the Kafka topic.
   - Fetches transaction details using Web3.
   - Analyzes gas usage and stores the data in PostgreSQL.

3. **PostgreSQL**:
   - Stores processed transaction details in the `transactionanalysis` table.
