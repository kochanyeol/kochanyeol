from pydantic import BaseModel, Field

class Product(BaseModel):
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "상품의 이름을 입력하세요",
                "price": 1000,
                "description": "상품 설명"
            }
        }
    }
    name: str
    price: float | int = Field(gt=0)
    description: str = "No description"
    # gt=0 → 0보다 큰 (greater than)
    # ge=0 → 0 이상 (greater than or equal)
    # lt=100 → 100보다 작은 (less than)
    # le=100 → 100 이하 (less than or equal)