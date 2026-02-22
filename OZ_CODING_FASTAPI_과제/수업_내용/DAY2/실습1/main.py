from pydantic import BaseModel, Field
from typing import List

class Item(BaseModel):
    name: str
    quantity: int = Field(ge=1)

class Order(BaseModel):
    id: int
    total_price: float = Field(gt=0)
    items: List[Item] = Field(default_factory=list)

from fastapi import FastAPI

app = FastAPI()

@app.post("/orders/")
def create_order(order: Order):
    return {"order": order}