# grpc_client_order_service.py
import grpc
import product_pb2
import product_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")
stub = product_pb2_grpc.ProductServiceStub(channel)

response = stub.GetProduct(product_pb2.ProductRequest(id=1))
print("Product:", response)
