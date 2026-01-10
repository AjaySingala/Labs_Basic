# shipping_service.py
import json
import time

print("Shipping Service Started...")
while True:
    try:
        with open("event_bus.json") as f:
            event = json.load(f)
            if event["event"] == "ORDER_CREATED":
                print("Shipping Order:", event["order_id"])
                break
    except:
        pass
    time.sleep(1)
