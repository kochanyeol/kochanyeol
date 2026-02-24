# [문제] Cart와 Product 모델 정의하기
#
# Product 모델
# 필드: name (문자열), price (소수, 0 이상), stock (정수, 0 이상)
# Cart 모델
# 필드: user_id (정수), products (여러 개의 Product 객체 → List 사용), total_amount (소수, 0 이상)
# /cart/ 로 POST 요청을 받아 장바구니 데이터를 생성하는 API 작성
# 최소 1개의 상품을 포함하는 요청 JSON 작성.

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float = Field(ge=0, description="0원 이상 입력해주세요.")
    stock: int = Field(ge=0, description="0 이상 입력해주세요.")

class Cart(BaseModel):
    user_id: int
    products: List[Product] = Field(default_factory=list)
    total_amount: float = Field(ge=0, description="0원 이상 입력해주세요.")

@app.post("/cart/")
def create_cart(cart: Cart):
    return {"cart": cart}