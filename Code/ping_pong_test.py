'''
description:  This file is used to ping pong test and produce diagrams
author: ywang531@@hawk.iit.edu
CWID: A20496705
'''
import time
import threading
from client_api import Publisher, Subscriber
import matplotlib.pyplot as plt

def ping_pong_client(publisher, subscriber, pid, sid, send_topic, receive_topic, num_messages):
    for i in range(num_messages):
        message = f"Ping {i}"
        # make sure to send the pid, topic, and message
        publisher.send(pid, send_topic, message)
        print(f"Sent: {message}")

        messages = subscriber.pull(sid, receive_topic)
        if messages:
            print("Received messages:", messages)
        else:
            print("No new messages.")
        # mock processing by sleeping for 100ms
        time.sleep(0.1)

def run_ping_pong_test(num_pairs, num_messages):
    threads = []
    for i in range(num_pairs):
        publisher = Publisher()
        subscriber = Subscriber()
        pid = publisher.registerPublisher()
        sid = subscriber.registerSubscriber()
        send_topic = f"topic_send_{i}"
        receive_topic = f"topic_send_{i}"
        publisher.createTopic(pid, send_topic)
        subscriber.subscribe(sid, receive_topic)

        thread = threading.Thread(target=ping_pong_client, args=(publisher, subscriber, pid, sid, send_topic, receive_topic, num_messages))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def plot_results(client_counts, results):
    plt.figure(figsize=(10, 5))
    plt.plot(client_counts, results, marker='o', linestyle='-', color='b')
    plt.title('Ping-Pong Test Throughput')
    plt.xlabel('Number of Publisher-Subscriber Pairs')
    plt.ylabel('Throughput (messages per second)')
    plt.grid(True)
    plt.savefig('../Misc/ping_pong_throughput.png')
    plt.close()

if __name__ == "__main__":
    num_messages = 100
    pairs_counts = [2, 32, 64, 128, 256, 512]
    throughputs = []
    
    for num_pairs in pairs_counts:
        start_time = time.time()
        run_ping_pong_test(num_pairs, num_messages)
        end_time = time.time()
        elapsed_time = end_time - start_time
        throughput = (num_pairs * num_messages) / elapsed_time
        throughputs.append(throughput)
        print(f"{num_pairs} pairs: Throughput = {throughput} messages/sec")

    plot_results(pairs_counts, throughputs)
