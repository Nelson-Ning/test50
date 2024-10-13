# Publisher-Subscriber System

This project implements a basic publisher-subscriber system with a message broker server that handles connections and message distribution between clients. It includes several Python scripts that act as the server, clients, and testing tools.

## Files Description

- `server.py`: This is the message broker server program. It handles incoming connections from clients, manages topics, and distributes messages among subscribers and publishers. It supports handling multiple client connections simultaneously using threading.

- `client_api.py`: A Python module that provides client-side API for interacting with the server. It includes two classes, `Publisher` and `Subscriber`, which handle the registration, topic creation, message sending, and message pulling.

- `publisher_client.py`: A client program that acts as a publisher. It uses the `client_api.py` to register as a publisher, create topics, and send messages to those topics.

- `subscriber_client.py`: A client program that acts as a subscriber. It uses the `client_api.py` to register as a subscriber, subscribe to topics, and pull messages from those topics.

- `benchmark_create_topic.py`: A script designed to benchmark the server’s throughput and performance by simulating multiple publishers and subscribers and measuring the system's responsiveness and data handling capabilities.

- `benckmark_all_api.py`: One that tests the maximum throughput of all apis on the machine and produces a graph.

- `ping_pong_test.py`: This script performs the ping-pong test using any quantity client programs (as publishers and subscribers) and any quantity topics to measure message passing efficiency and server throughput under controlled conditions.

- `requirements.txt`: List of external libraries that python runs on

- `Makefile`: Encapsulates scripts including initializing the environment, cleaning the environment, and starting the publishing and subscribing server, and so on

## Environmental Setting and Operation Guide

Run the following command to create a Python virtual environment and install all necessary dependencies:

```bash
   make clean && make setup
```

**Note: The file does not contain the installation steps for Python 3.x itself, which can be easily searched on the network**

## Running the System

To run the system, follow these steps: 

**Note: Ensure that `make setup` has been executed**

1. Start the message broker server:
   **Note: Just need to execute once**
   ```bash
   make run-server
   ```

2. Open another terminal and run a publisher client:
   **Note: Can run multiple publishers**
   ```bash
   make run-publisher
   ```
3. Open another terminal and run a subscriber client:
   **Note: Can run multiple subscriber**
   ```bash
   make run-subscriber
   ```
4. To perform benchmarks and throughput tests (create_topic), run:
   **Note: Just need to execute once, The generated results will be in the `Misc` folder**
   ```bash
   make benchmark-create-topic
   ```
5. To perform benchmarks and throughput tests (all), run:
   **Note: Just need to execute once, The generated results will be in the `Misc` folder**
   ```bash
   make benchmark-all
   ```
6. To perform ping-pong tests, run:
   **Note: Just need to execute once, The generated results will be in the `Misc` folder**
   ```bash
   make ping-pong-test
   ```

### Additional Notes
Ensure all scripts are executed in an environment where Python 3.x is installed and available

### Author
ywang531@hawk.iit.edu A20496705