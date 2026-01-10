# order_service_http.py
from fastapi import FastAPI
import httpx

app = FastAPI(title="Order Service")

PRODUCT_SERVICE = "http://localhost:8000/products"

orders = [
    {"order_id": 101, "product_id": 1, "qty": 2},
    # {"order_id": 102, "product_id": 2, "qty": 5},
    # {"order_id": 103, "product_id": 3, "qty": 1},
]

@app.get("/orders/details")
async def get_order_details():
    async with httpx.AsyncClient() as client:
        for order in orders:
            res = await client.get(f"{PRODUCT_SERVICE}/{order['product_id']}")
            order["product"] = res.json()
    return orders
