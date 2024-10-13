'''
description:  This file defines the publisher and subscriber classes.
author: ywang531@@hawk.iit.edu
CWID: A20496705
'''
import socket
import json

def create_topic(host, port, topic):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        request = json.dumps({"action": "createTopic", "topic": topic})
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        client_socket.close()
        return response
    except Exception as e:
        return str(e)

class ClientBase:
    def __init__(self, host='localhost', port=12345):
        # Connect to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    # Send request to server and get response
    def send_request(self, data):
        # Send data to server
        self.client_socket.sendall(json.dumps(data).encode('utf-8'))
        # Get response from server
        response = self.client_socket.recv(1024).decode('utf-8')
        # Return response
        return json.loads(response)

    def close(self):
        # Close socket
        self.client_socket.close()

class Publisher(ClientBase):
    # Register publisher
    def __init__(self, host='localhost', port=12345):
        super().__init__(host, port)
        # Get PID
        self.pid = self.registerPublisher()

    # API for assignment requirements (1): Publisher: <PID> registerPublisher(); 
    def registerPublisher(self):
        # Request PID
        request = {"action": "registerPublisher"}
        # Send request
        response = self.send_request(request)
        # Return PID
        return response["pid"]

    # API for assignment requirements (2): Publisher: createTopic (PID, String topic); 
    def createTopic(self, pid, topic):
        # Create topic
        request = {"action": "createTopic", "pid": pid, "topic": topic}
        # Send request
        self.send_request(request)

    # API for assignment requirements (3): Publisher: deleteTopic (PID, String topic);
    def deleteTopic(self, pid, topic):
        # Delete topic
        request = {"action": "deleteTopic", "pid": pid, "topic": topic}
        response = self.send_request(request)
        # Print success message if topic successfully deleted
        if response and "status" in response and response["status"] == "Topic deleted":
            print(f"Topic '{topic}' successfully deleted.")
        else:
            print(f"Failed to delete topic '{topic}'.")
        
    # API for assignment requirements (4): Publisher: send (PID, String topic, String message);; 
    def send(self, pid, topic, message):
        # Send message
        request = {"action": "send", "pid": pid, "topic": topic, "message": message}
        # Send request
        self.send_request(request)

class Subscriber(ClientBase):
    # Register subscriber
    def __init__(self, host='localhost', port=12345):
        # Connect to server
        super().__init__(host, port)
        # Get SID
        self.sid = self.registerSubscriber()

    # API for assignment requirements (5): Subscriber: <SID> registerSubscriber ();
    def registerSubscriber(self):
        # Request SID
        request = {"action": "registerSubscriber"}
        # Send request
        response = self.send_request(request)
        # Return SID
        if response and "sid" in response:
            return response["sid"]
        else:
            raise Exception("Failed to register subscriber")

    # API for assignment requirements (6): Subscriber: <SID> subscribe (String topic);
    def subscribe(self, sid, topic):
        # Subscribe to topic
        request = {"action": "subscribe", "sid": sid, "topic": topic}
        # Send request
        response = self.send_request(request)
        # Print success message if topic successfully subscribed
        if not response or "status" not in response or response["status"] != "Subscribed to " + topic:
            print(f"Failed to subscribe to {topic}")
        else:
            print(f"Successfully subscribed to {topic}")

    # API for assignment requirements (7): Subscriber: <SID> List <String> pull (SID, String topic);
    def pull(self, sid, topic):
        request = {"action": "pull", "sid": sid, "topic": topic}
        response = self.send_request(request)
        if response is None or "messages" not in response:
            # Print error message if no messages available
            print("Failed to pull messages or no messages available.")
            return []
        return response["messages"]
