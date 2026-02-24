from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from typing import List
import asyncio
import uuid
import re
import random

from pydantic_core.core_schema import computed_field

""" 1번 문제 """

# 1. 다중 필드 조건 검증
# Ticket 모델을 정의하고 /tickets/ POST API를 만드세요.
#
# 필드: name(str), age(int), ticket_type(str)
# ticket_type이 "adult"면 age가 18 이상이어야 함
# ticket_type이 "child"면 age가 17 이하여야 함
# ticket_type이 "adult" 또는 "child"만 허용

class Ticket(BaseModel):
    name: str
    age: int
    ticket_type: str

    @model_validator(mode="after")
    def user_validator(self):
        if self.ticket_type not in ["adult", "child"]:
            raise ValueError("adult 또는 child 중 하나를 입력해주세요")
        if self.ticket_type == "adult" and self.age < 18:
            raise ValueError("adult는 18세 이상이어야 합니다")
        if self.ticket_type == "child" and self.age > 17:
            raise ValueError("child는 17세 이하여야 합니다")
        return self

@app.post("/tickets/")
def create_ticket(ticket: Ticket):
    return ticket

""" 2번 문제 """

# 2. 중첩 모델 + computed_field
# Order와 OrderItem 모델을 정의하고 /orders/ POST API를 만드세요.
#
# OrderItem 필드: name(str), price(float, 0 이상), quantity(int, 1 이상)
# Order 필드: order_id(str, UUID 자동 생성), items(List[OrderItem])
# total_price는 자동 계산 (모든 items의 price * quantity 합산)

class OrderItem(BaseModel):
    name: str
    price: float = Field(ge=0)
    quantity: int = Field(ge=1)

class Order(BaseModel):
    order_id: str = Field(default_factory=lambda:str(uuid.uuid4()))
    items: List[OrderItem]

    @computed_field
    @property
    def total_price(self) -> float:
        return sum(item.price * item.quantity for item in self.items)

@app.post("/orders/")
def create_order(order: Order):
    return order

""" 3번 문제 """

# 3. 비밀번호 강도 검증
# SecureUser 모델을 정의하고 /secure-users/ POST API를 만드세요.
#
# 필드: username(str), password(str)
# 비밀번호는 8자 이상, 대문자 1개 이상, 숫자 1개 이상 포함 필수 (re 사용)

PASSWORD_REGEX = r'^(?=.*[A-Z])(?=.*[0-9]).{8,}$'

class SecureUser(BaseModel):
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def password_validator(cls, v):
        if not re.match(PASSWORD_REGEX, v):
            raise ValueError("올바르게 입력해주세요.")

@app.post("/secure-users/")
def create_secure_user(secure_user: SecureUser):
    return secure_user

""" 4번 문제 """

# 4. 역할 기반 접근 제한
# AdminUser 모델을 정의하고 /admin/ POST API를 만드세요.
#
# 필드: username(str), role(str), access_level(int, 1~5)
# role이 "admin"이면 access_level이 4 이상이어야 함
# role이 "user"면 access_level이 3 이하여야 함

class AdminUser(BaseModel):
    username: str
    role: str
    access_level: int = Field(ge=1, le=5)

    @model_validator(mode="after")
    def role_validator(self):
        if self.role == "admin" and self.access_level < 3:
            raise ValueError("admin은 access_level 4이상이여야 합니다.")
        if self.role == "user" and self.access_level > 4:
            raise ValueError("user은 access_level 3이하이여야 합니다.")
        return self

@app.post("/admin/")
def create_admin(admin: AdminUser):
    return admin

""" 5번 문제 """

# 5. 다중 validator 조합
# BankAccount 모델을 정의하고 /accounts/ POST API를 만드세요.
#
# 필드: owner(str), account_number(str), balance(float)
# account_number는 정확히 14자리 숫자 (re 사용)
# balance는 0 이상
# owner 이름은 소문자로 변환 후 공백 제거 (strip)

ACCOUNT_REGEX = r"^[0-9]{14}$"


class BankAccount(BaseModel):
    owner: str
    account_number: str
    balance: float = Field(ge=0)

    @field_validator("owner")
    @classmethod
    def owner_validator(cls, v):
        return v.lower().strip()

    @field_validator("account_number")
    @classmethod
    def account_validator(cls, v):
        if not re.match(ACCOUNT_REGEX, v):
            raise ValueError("14자리를 입력하세요.")
        return v

@app.post("/accounts/")
def create_account(account: BankAccount):
    return account

""" 6번 문제 """

# 6. 조건부 필수 필드
# Delivery 모델을 정의하고 /deliveries/ POST API를 만드세요.
#
# 필드: recipient(str), delivery_type(str), address(str | None), pickup_location(str | None)
# delivery_type이 "home"이면 address 필수
# delivery_type이 "pickup"이면 pickup_location 필수

class Delivery(BaseModel):
    recipient: str
    delivery_type: str
    address: str | None
    pickup_location: str | None

