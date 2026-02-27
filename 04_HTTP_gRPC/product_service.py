# product_service.py  (enhanced)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Product Service with Validation")

class Product(BaseModel):
    id: int
    name: str
    price: float

#products: Dict[int, Product] = {}
products = {
    1: ("Laptop", 2000),
    2: ("Mobile", 1000)
}

@app.post("/products")
def create_product(product: Product):
    if product.id in products:
        raise HTTPException(status_code=400, detail="Product already exists")
    products[product.id] = product
    return product

@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return products[product_id]

