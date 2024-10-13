'''
description: This file is responsible for running the message proxy server, handling connections and requests from clients.
author: ywang531@@hawk.iit.edu
CWID: A20496705
'''

import socket
import threading
import json

# Message Broker
class MessageBroker:
    # Initialize server
    def __init__(self, host='localhost', port=12345):
        # Define host and port
        self.host = host
        self.port = port
        # Define clients and topics
        self.clients = {}
        self.topics = {}
        # Define lock
        self.lock = threading.Lock()

    # Start Server
    def start(self):
        # Create socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Bind socket to address
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            # Listen for connections
            print(f"Server listening on {self.host}:{self.port}")
            while True:
                #  Accept connection
                client_socket, addr = server_socket.accept()
                # Start new thread for client
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    # Handle client
    def handle_client(self, client_socket):
        # Receive data
        with client_socket:
            while True:
                try:
                    # Receive data
                    data = client_socket.recv(1024).decode()
                    if not data:
                        break
                    # Process request
                    self.process_request(data, client_socket)
                except ConnectionResetError:
                    break

    # message processing
    def process_request(self, data, client_socket):
        request = json.loads(data)
        action = request["action"]
        if action == "registerPublisher":
            # Get PID
            pid = str(id(client_socket))
            # Add PID to list of clients
            self.clients[pid] = client_socket
            # Send PID back to client
            response = {"pid": pid}
            # Send response
            print("Sending response:", response)
            client_socket.sendall(json.dumps(response).encode('utf-8'))
        elif action == "createTopic":
            topic = request["topic"]
            # make sure topic is a dictionary with a list of messages and a list of subscribers
            if topic not in self.topics:
                # initialize topic if it doesn't exist
                self.topics[topic] = {"messages": [], "subscribers": {}}
            response = {"status": "Topic created"}
            print("Sending response:", response)
            client_socket.sendall(json.dumps(response).encode('utf-8'))
        elif action == "subscribe":
            sid = request["sid"]
            topic = request["topic"]
            if topic in self.topics:
                if sid not in self.topics[topic]["subscribers"]:
                    self.topics[topic]["subscribers"][sid] = 0
                response = {"status": "Subscribed to " + topic}
            else:
                response = {"status": "Topic not found"}

            print("Sending response:", response)
            client_socket.sendall(json.dumps(response).encode('utf-8'))
        elif action == "send":
            topic = request["topic"]
            message = request["message"]
            if topic in self.topics:
                # Add message to topic
                self.topics[topic]["messages"].append(message)
            response = {"status": "Message sent: " + message}
            print("Sending response:", response)
            client_socket.sendall(json.dumps(response).encode('utf-8'))
        elif action == "registerSubscriber":
            # Get SID
            sid = str(id(client_socket))
            self.clients[sid] = client_socket
            response = {"sid": sid}
            print("Sending response:", response)
            client_socket.sendall(json.dumps(response).encode('utf-8'))
        elif action == "pull":
            sid = request["sid"]
            topic = request["topic"]
            messages = []
            if topic in self.topics and sid in self.topics[topic]["subscribers"]:
                # find messages since last pull
                start_index = self.topics[topic]["subscribers"][sid]
                messages = self.topics[topic]["messages"][start_index:]
                # update index for next pull
                self.topics[topic]["subscribers"][sid] = len(self.topics[topic]["messages"])
            response = {"messages": messages}
            print("Sending response:", response)
            client_socket.sendall(json.dumps(response).encode('utf-8'))

if __name__ == "__main__":
    broker = MessageBroker()
    broker.start()
