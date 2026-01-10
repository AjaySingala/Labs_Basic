# order_service.py
from fastapi import FastAPI

app = FastAPI(title="Order Service")

orders = [
    {"order_id": 101, "product_id": 1, "qty": 2},
    {"order_id": 102, "product_id": 2, "qty": 1},
]

@app.get("/orders")
def get_orders():
    return orders
