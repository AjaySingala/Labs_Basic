# product_service.py
from fastapi import FastAPI, HTTPException
from typing import Dict

app = FastAPI(title="Product Service")

products: Dict[int, dict] = {
    1: {"id": 1, "name": "Laptop", "price": 55000},
    2: {"id": 2, "name": "Mobile", "price": 20000},
}

@app.get("/products")
def get_products():
    return list(products.values())

@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return products[product_id]
