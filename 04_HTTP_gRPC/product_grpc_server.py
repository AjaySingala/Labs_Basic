# product_grpc_server.py
import grpc
from concurrent import futures
import product_pb2
import product_pb2_grpc

products = {
    1: ("Laptop", 55000),
    2: ("Mobile", 20000)
}

class ProductService(product_pb2_grpc.ProductServiceServicer):
    def GetProduct(self, request, context):
        name, price = products.get(request.id, ("Unknown", 0))
        return product_pb2.ProductResponse(id=request.id, name=name, price=price)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
