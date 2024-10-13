'''
description: This file is used to perform performance tests for create topic and produce diagrams
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
def client_thread(host, port, num_requests, results, index):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    start_time = time.time()
    
    # for loop to create topic
    for i in range(num_requests):
        topic_name = f"topic_{i}"
        request = json.dumps({"action": "createTopic", "topic": topic_name}).encode('utf-8')
        client_socket.sendall(request)
        # receive response
        response = client_socket.recv(1024).decode('utf-8')
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    results[index] = elapsed_time

    return elapsed_time

# run benchmark
def run_benchmark(num_clients, num_requests_per_client):
    threads = []
    # create a list to store the results of each thread
    results = [None] * num_clients

    for _ in range(num_clients):
        thread = threading.Thread(target=client_thread, args=(host, port, num_requests_per_client, results, _))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return results

if __name__ == "__main__":
    client_counts = [1, 150, 256, 512]
    num_requests_per_client = [10, 50, 100]
    all_results = {}

    for client_count in client_counts:
        for num_requests in num_requests_per_client:
            print(f"Testing with {client_count} clients each making {num_requests} requests...")
            results = run_benchmark(client_count, num_requests)
            all_results[(client_count, num_requests)] = results
    
    total_times = {}
    for key, times in all_results.items():
        total_times[key] = sum(times)

    plt.figure(figsize=(10, 5))
    for key, total_time in total_times.items():
        plt.plot(key[0], total_time, 'o', label=f'{key[0]} clients, {key[1]} reqs')

    plt.title('Total Execution Time for Varying Client Counts and Request Volumes')
    plt.xlabel('Number of Clients')
    plt.ylabel('Total Time Taken (seconds)')
    plt.legend()
    plt.grid(True)
    plt.savefig('../Misc/total_execution_time_by_client_count_and_requests_create_topic.png')
    plt.close()
