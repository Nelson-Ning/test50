'''
description: An example of a subcriber client that uses the client_api.py file
author: ywang531@@hawk.iit.edu
CWID: A20496705
'''

import time
from client_api import Subscriber

def main():
    # register a subscriber
    subscriber = Subscriber()
    sid = subscriber.registerSubscriber()
    # register a topic: news
    topic = "news"

    # subscribe to topic
    subscriber.subscribe(sid, topic)
    # print the topic
    print(f"Subscribed to {topic}")

    try:
        while True:
            # pull messages from topic
            messages = subscriber.pull(sid, topic)
            if messages:
                # print messages
                print("Received messages:", messages)
            else:
                # no new messages
                print("No new messages.")
            time.sleep(1)  # sleep 1 second
    except KeyboardInterrupt:
        # Ctrl+C pressed
        print("Exiting...")
    finally:
        # close the subscriber
        subscriber.close()

if __name__ == "__main__":
    main()
