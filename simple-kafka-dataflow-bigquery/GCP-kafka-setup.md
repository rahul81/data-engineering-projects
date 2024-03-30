# Setting Up a Kafka Cluster on GCP VM Using Docker

In the world of real-time data processing and streaming, Apache Kafka stands as a robust and widely-used platform. Setting up a Kafka cluster on Google Cloud Platform (GCP) VM can be a crucial step in building your data processing pipeline. In this guide, we'll walk through the process of deploying a Kafka cluster on a GCP VM using Docker.

## Prerequisites

Before diving into the setup process, ensure that you have the following prerequisites in place:

- A GCP VM instance up and running.
- SSH access to your GCP VM.
- Basic knowledge of Docker and Docker Compose.

## Step 1: Remove Conflicting Packages

To ensure a smooth installation, it's essential to remove any conflicting packages that might interfere with Docker. Run the following commands on your GCP VM:

```bash
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

## Step 2: Install Docker

Docker is at the heart of containerization and will be used to run Kafka in containers on your GCP VM. Follow these steps to install Docker:

### Add Docker's Official GPG Key

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

### Add the Docker Repository to Apt Sources

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Run Update

```bash
sudo apt-get update
```

### Install Docker

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## A look inside the docker-compose file

```yml
---
version: '3'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    hostname: zookeeper
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  broker:
    image: confluentinc/cp-server:latest
    hostname: broker
    container_name: broker
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
      - "9101:9101"
      - "9094:9094"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_LISTNERS: INTERNAL://:29092,LOCAL://:9092,EXTERNAL://:9094
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,LOCAL:PLAINTEXT,EXTERNAL:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: INTERNAL://broker:29092,LOCAL://localhost:9092,EXTERNAL://VM_IP:9094
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_METRIC_REPORTERS: io.confluent.metrics.reporter.ConfluentMetricsReporter
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_CONFLUENT_LICENSE_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_CONFLUENT_BALANCER_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_JMX_PORT: 9101
      KAFKA_JMX_HOSTNAME: localhost
      CONFLUENT_METRICS_REPORTER_BOOTSTRAP_SERVERS: broker:29092
      CONFLUENT_METRICS_REPORTER_TOPIC_REPLICAS: 1
      CONFLUENT_METRICS_ENABLE: 'true'
      CONFLUENT_SUPPORT_CUSTOMER_ID: 'anonymous'

  broker2:
    image: confluentinc/cp-server:latest
    hostname: broker2
    container_name: broker2
    depends_on:
      - zookeeper
    ports:
      - "9093:9093"
      - "9102:9102"
      - "9095:9095"
    environment:
      KAFKA_BROKER_ID: 2
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_LISTNERS: INTERNAL://:29093,LOCAL://:9093,EXTERNAL://:9095
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,LOCAL:PLAINTEXT,EXTERNAL:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: INTERNAL://broker2:29093,LOCAL://localhost:9093,EXTERNAL://VM_IP:9095
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_METRIC_REPORTERS: io.confluent.metrics.reporter.ConfluentMetricsReporter
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_CONFLUENT_LICENSE_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_CONFLUENT_BALANCER_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_JMX_PORT: 9102
      KAFKA_JMX_HOSTNAME: localhost
      CONFLUENT_METRICS_REPORTER_BOOTSTRAP_SERVERS: broker2:29092
      CONFLUENT_METRICS_REPORTER_TOPIC_REPLICAS: 1
      CONFLUENT_METRICS_ENABLE: 'true'
      CONFLUENT_SUPPORT_CUSTOMER_ID: 'anonymous'

  control-center:
    image: confluentinc/cp-enterprise-control-center:latest
    hostname: control-center
    container_name: control-center
    depends_on:
      - broker
    ports:
      - "9021:9021"
    environment:
      CONTROL_CENTER_BOOTSTRAP_SERVERS: 'broker:29092,boker2:29093'
      CONTROL_CENTER_REPLICATION_FACTOR: 1
      CONTROL_CENTER_INTERNAL_TOPICS_PARTITIONS: 1
      CONTROL_CENTER_MONITORING_INTERCEPTOR_TOPIC_PARTITIONS: 1
      CONFLUENT_METRICS_TOPIC_REPLICATION: 1
      PORT: 9021

```

This Docker Compose file defines a setup for running Apache Kafka with Confluent Control Center. It consists of three services:

### Zookeeper

- **Purpose**: Zookeeper is a centralized service used for maintaining configuration information, naming, providing distributed synchronization, and group services within a Kafka cluster.
- **Functionality**: It plays a crucial role in managing distributed systems, ensuring data consistency and coordination among different components of the Kafka cluster.
- **Configuration**: 
  - Exposes port 2181 for client connections.
  - Sets environment variables for Zookeeper client port and tick time.

### Broker

- **Purpose**: The Kafka broker is the core component of the Kafka ecosystem responsible for message storage, replication, and serving consumer requests.
- **Functionality**: It handles the storage and retrieval of Kafka topics, replication of data across multiple brokers for fault tolerance, and communication with clients (producers and consumers).
- **Configuration**: 
  - Defines various listener ports for different types of connections (internal, local, external).
  - Configures Kafka broker ID, Zookeeper connection, advertised listeners for external access, and other Kafka-specific settings.
  - Enables metrics reporting and sets up JMX port for monitoring.
  - multiple kafka brokers can be configured by adding more broker instances to the docker-compose file like broker2 in this example

### Control Center

- **Purpose**: Confluent Control Center is a management and monitoring tool for Kafka clusters, providing a centralized interface for managing Kafka resources, monitoring performance, and tracking data flows.
- **Functionality**: It offers features like real-time monitoring, alerting, centralized configuration management, and a user-friendly interface for Kafka administrators.
- **Configuration**: 
  - Specifies bootstrap servers for Control Center to connect to Kafka.
  - Sets up configurations for replication, topic partitions, and metrics to ensure smooth operation and monitoring.
  - Exposes port 9021 for web UI access to Control Center.

*note*: 
- Make sure to replace the VM_IP with actual IP of your GCP VM to be able to send and recieve messages.
- Make sure in your VPC network protocol HTPP requests are allowed.


## Step 3: Start the Kafka Cluster

With Docker installed, it's time to launch your Kafka cluster. Ensure that you have a `docker-compose.yaml` file ready on your GCP VM. This file contains the configuration for your Kafka setup. Make sure to copy the `docker-compose.yaml` file to your GCP VM before executing the following command:

```bash
sudo docker compose -f "docker-compose.yaml" up -d --build
```

This command will start your Kafka cluster in detached mode, allowing it to run in the background.

Once the Kafka cluster is up and running you can access the Kafka Cluster WebUi on the url http://<vm public ip>:9021

Congratulations! You've successfully set up a Kafka cluster on your GCP VM using Docker. You can now proceed to configure Kafka producers and consumers to start streaming data, and even integrate it with Google Dataflow to write data to BigQuery for further analysis and processing.

Here is the [Github link](https:github.com/rahul81) for the docker-compose file along with Producer and Consumer files to get started with sending and recieving messages to Kafka Cluster.


