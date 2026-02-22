from temp import Product
from fastapi import FastAPI

app = FastAPI()

@app.post("/products/")
async def post_product(product: Product):
    return {"product": product}