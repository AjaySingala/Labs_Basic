# secure_product_service.py
from fastapi import FastAPI, HTTPException, Header

app = FastAPI(title="Secure Product Service")

API_KEY = "TRAINING123"

@app.get("/v1/products")
def get_products(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return [
        {"id": 1, "name": "Laptop"},
        {"id": 2, "name": "Mobile"}
    ]
