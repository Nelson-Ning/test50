'''
description: An example of a publisher client that uses the client_api.py file
author: ywang531@@hawk.iit.edu
CWID: A20496705
'''

from client_api import Publisher

publisher = Publisher()
# register a Publisher
pid = publisher.registerPublisher()
# create a topic
publisher.createTopic(pid, "news")
# send a message: "Hello, world"
publisher.send(pid, "news", "Hello, world")
