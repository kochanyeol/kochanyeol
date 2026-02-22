from fastapi import FastAPI
from pydantic import BaseModel, computed_field, field_validator

app = FastAPI()


class Product(BaseModel):
    name: str
    price: float
    discount: float = 0

    @field_validator("discount")
    @classmethod
    def validate_discount(cls, value):
        if not (0 <= value <= 100):
            raise ValueError("할인율은 0-100% 사이")
        return value

    @computed_field
    @property
    def final_price(self) -> float:
        return round(self.price * (1 - self.discount / 100), 1)


@app.post("/products")
def create_product(product: Product):
    return product