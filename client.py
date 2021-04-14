# -*- coding: utf-8 -*-

import logging

from opcua import Client
from time import sleep
from IPython import embed


class SubHandler(object):

    """
    Client to subscription. It will receive events from server
    
    tags: list of all processed network nodes;
    storage: multilist for recording the values of processed nodes;
    
    """

    def __init__(self, tags):   
        self.tags = tags
        self.storage = [ [] for i in range(len(tags)) ]

    def datachange_notification(self, node, val, data):
       i = self.tags.index(node)
       self.storage[i].append(val)
       
       print("Python: New data change event", node, val)
            
    def event_notification(self, event):
        print("Python: New event", event)


def main():
    logging.basicConfig(level=logging.WARN)
    client = Client("opc.tcp://WIN-B3JSS0UOON2:49320")
    try:
        client.connect()

        tag1 = client.get_node("ns=2;s=Channel1.Device1.Tag1")
        tag2 = client.get_node("ns=2;s=Simulation Examples.Functions.Ramp3")
        tag3 = client.get_node("ns=2;s=Simulation Examples.Functions.Sine1")
        
        tags = [tag1, tag2, tag3]
  
        handler = SubHandler(tags)
        sub = client.create_subscription(0, handler)
        
        handle1 = sub.subscribe_data_change(tag1)
        handle2 = sub.subscribe_data_change(tag2)
        handle3 = sub.subscribe_data_change(tag3)

        sleep(0.1)

        embed()

    finally:
        client.disconnect()
        print(handler.storage)


if __name__ == "__main__":
    main()
