# -*- coding: utf-8 -*-

import logging

from opcua import Client
from time import sleep
from IPython import embed


class SubHandler(object):

    """
    Client to subscription. It will receive events from server
    """
    
    def __init__(self):
        self.storage = []

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)
        self.storage.append(val)
        
 
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
        
        handler1 = SubHandler()
        sub1 = client.create_subscription(0, handler1)
        sub1.subscribe_data_change(tag1)
        
        handler2 = SubHandler()
        sub2 = client.create_subscription(0, handler2)
        sub2.subscribe_data_change(tag2)
        
        handler3 = SubHandler()
        sub3 = client.create_subscription(0, handler3)
        sub3.subscribe_data_change(tag3)
        
        sleep(0.1)
        
        embed()
    finally:
        client.disconnect()
        print("___1___", handler1.storage)
        print("___2___", handler2.storage)
        print("___3___", handler3.storage)
        

if __name__ == "__main__":
    main()

