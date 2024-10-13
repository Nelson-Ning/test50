'''
description: This file is used to perform performance tests for all api and produce diagrams
author: ywang531@@hawk.iit.edu
CWID: A20496705
'''

import threading
import socket
import json
import time
import matplotlib.pyplot as plt

host = 'localhost'
port = 12345

# create a test function that creates a topic and then publishes a message to that topic
def client_thread(host, port, num_requests, results, index, action, extra_data=None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    start_time = time.time()
    
    # send request for each action
    for i in range(num_requests):
        if action == "createTopic":
            topic_name = f"topic_{index}_{i}"
            request = {"action": action, "topic": topic_name}
        elif action == "registerPublisher":
            request = {"action": action}
        elif action == "subscribe":
            request = {"action": action, "sid": extra_data, "topic": f"topic_{index}_{i}"}
        elif action == "send":
            request = {"action": action, "topic": extra_data, "message": f"Message {i}"}
        elif action == "pull":
            request = {"action": action, "sid": extra_data, "topic": f"topic_{index}_{i}"}
        request = json.dumps(request).encode('utf-8')
        client_socket.sendall(request)
        response = client_socket.recv(1024).decode('utf-8')
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    results[index] = elapsed_time

# run benchmark
def run_benchmark(num_clients, num_requests_per_client, action, extra_data=None):
    threads = []
    results = [None] * num_clients
    for i in range(num_clients):
        thread = threading.Thread(target=client_thread, args=(host, port, num_requests_per_client, results, i, action, extra_data))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return results

# print results by plt
def plot_results(actions, results):
    plt.figure(figsize=(10, 5))
    for action, res in results.items():
        plt.plot(res.keys(), res.values(), 'o-', label=f'Action: {action}')
    
    plt.title('Benchmark Results for Various Actions')
    plt.xlabel('Number of Clients')
    plt.ylabel('Time Taken (seconds)')
    plt.legend()
    plt.grid(True)
    plt.savefig('../Misc/benchmark_results_for_various_actions.png')
    plt.close()

# main
if __name__ == "__main__":
    client_counts = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    num_requests_per_client = 100
    # all need to be test action of lists
    actions = ["registerPublisher", "createTopic", "subscribe", "send", "pull"]
    all_results = {action: {} for action in actions}

    for action in actions:
        for client_count in client_counts:
            print(f"Testing {action} with {client_count} clients...")
            results = run_benchmark(client_count, num_requests_per_client, action)
            all_results[action][client_count] = sum(results) / len(results)
    
    plot_results(actions, all_results)
