# grpc_client_order_service.py
import grpc
#from InterServiceComms.Saga.saga import order
import product_pb2
import product_pb2_grpc

#gRPC call.
channel = grpc.insecure_channel("localhost:50051")
stub = product_pb2_grpc.ProductServiceStub(channel)

response = stub.GetProduct(product_pb2.ProductRequest(id=1))
print("Product:", response)

# HTTP call.
PRODUCT_SERVICE = "http://localhost:8000/products"

orders = [
    {"order_id": 101, "product_id": 1, "qty": 2},
    {"order_id": 102, "product_id": 2, "qty": 5},
    {"order_id": 103, "product_id": 3, "qty": 1},
]

import requests

def get_order_details():
    for order in orders:
        response = requests.get(f"{PRODUCT_SERVICE}/{order['product_id']}")
        data = response.json()
        order["product"] = data
    return orders

print(get_order_details())
