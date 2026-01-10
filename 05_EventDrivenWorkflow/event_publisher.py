# event_publisher.py
import json
import time

def publish_event():
    event = {"event": "ORDER_CREATED", "order_id": 101}
    with open("event_bus.json", "w") as f:
        json.dump(event, f)
    print("Event Published")

publish_event()
