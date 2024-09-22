# CDC Pipeline with Kafka, Debezium, PostgreSQL, and Docker

This repository contains a setup for a **Change Data Capture (CDC) pipeline** using **Kafka**, **Debezium**, **PostgreSQL**, and **Docker**. CDC enables real-time streaming of database changes (inserts, updates, deletes) from PostgreSQL into Kafka topics. This stack can be used for building real-time analytics, data synchronization, and event-driven architectures.

### Stack Overview:
- **Zookeeper**: Manages Kafka cluster metadata.
- **Kafka**: A distributed event streaming platform where PostgreSQL changes are streamed.
- **Debezium**: Captures changes from PostgreSQL and pushes them into Kafka.
- **PostgreSQL**: The source database where changes are tracked.
- **Schema Registry**: Manages schemas for Avro serialization in Kafka.
- **Control Center**: A web-based UI for managing and monitoring the Kafka ecosystem.

### Prerequisites
- **Docker**: Docker is used to containerize and quickly deploy the entire CDC stack.

Make sure Docker is installed on your machine. If you don't have Docker installed, refer to the [official Docker installation guide](https://docs.docker.com/get-docker/).

### Getting Started

1. Clone this repository:
    ```bash
    git clone <repository-url>
    cd cdc-pipeline
    ```

2. Start the CDC stack using Docker Compose:
    ```bash
    docker-compose up -d
    ```

3. Access the Kafka Control Center UI:
   - Open your browser and go to `http://localhost:9021` to manage your Kafka cluster and Debezium connectors.

### What's Next?

After deploying the stack, you can set up a PostgreSQL connector via the Kafka Control Center UI to capture changes from your PostgreSQL database and publish them into Kafka topics.

Once the CDC pipeline is set up, you can experiment with:
- Running different database operations (inserts, updates, deletes) on PostgreSQL.
- Consuming messages from the Kafka topics to see real-time data streams.
- Integrating downstream applications such as **Apache Spark**, **Flink**, or syncing with data warehouses for real-time analytics.

Feel free to modify configurations, extend the setup, and build your own custom CDC pipelines!

---

### Stopping the Stack
To stop and remove the containers, run:
```bash
docker-compose down
