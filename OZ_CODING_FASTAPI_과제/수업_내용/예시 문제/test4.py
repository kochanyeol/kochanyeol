from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from typing import List
import asyncio
import uuid
import re
import random

app = FastAPI()

""" 1번 문제 """

# 1. model_validator - 비밀번호 확인
# UserRegister 모델을 정의하고 /register/ POST API를 만드세요.
#
# 필드: username(str), password(str), confirm_password(str)
# password와 confirm_password가 일치하지 않으면 에러 반환

class UserRegister(BaseModel):
    username: str
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def check_password(self):
        if not self.password == self.confirm_password:
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return self

@app.post("/register/")
def create_register(register: UserRegister):
    return {
        "username" : username,
        "password" : "비밀번호 설정완료"
    }

""" 2번 문제 """

# 2. field_validator - 전화번호 형식
# Contact 모델을 정의하고 /contacts/ POST API를 만드세요.
#
# 필드: name(str), phone(str)
# 전화번호는 010-XXXX-XXXX 형식만 허용 (re 사용)

PHONE_REGEX = r"^010-[0-9]{4}-[0-9]{4}$"

class Contact(BaseModel):
    name: str
    phone: str

    @field_validator("phone")
    @classmethod
    def validator_phone(cls, v):
        if not re.match(PHONE_REGEX, v):
            raise ValueError("올바른 형식으로 작성해주세요.")
        return v

@app.post("/contacts/")
def create_contacts(contact: Contact):
    return contact

""" 3번 문제 """

# 3. computed_field - 나이 자동 계산
# User 모델을 정의하고 /users/ POST API를 만드세요.
#
# 필드: name(str), birth_year(int)
# age는 자동으로 계산 (computed_field 사용)

class User(BaseModel):
    name: str
    birth_year: int

    @computed_field
    @property
    def age(self) -> int:
        return datetime.now().year - self.birth_year

@app.post("/users/")
def create_user(user: User):
    return user

""" 4번 문제 """

# 4. default_factory - 랜덤 인증코드
# Verification 모델을 정의하고 /verify/ POST API를 만드세요.
#
# 필드: email(str), code(str, 6자리 랜덤 숫자 자동 생성)
# 힌트: random 모듈 사용

class Verification(BaseModel):
    email: str
    code: str = Field(default_factory=lambda:str(random.ranint(100000,999999)))

@app.post("/verify/")
def create_verify(verify:Verification):
    return verify

""" 5번 문제 """

# 5. model_validator before/after 구분
# Product 모델을 정의하고 /products/ POST API를 만드세요.
#
# 필드: name(str), category(str)
# before: name과 category를 소문자로 변환
# after: name이 빈 문자열이면 에러 반환

class Product(BaseModel):
    name: str
    category: str

    @model_validator(mode="before")
    @classmethod
    def trans_validator(cls, data):
        if isinstance(data, dict):
            if data.get("name"):
                data["name"] = data["name"].lower()
        return data

    @model_validator(mode="after")
    def name_validator(self):
        if not self.name:
            raise ValueError("이름을 입력해주세요.")
        return self

@app.post("/products/")
def create_product(product: Product):
    return Product

""" 6번 문제"""

# 6. 중첩 모델 + List + 검증
# School과 Student 모델을 정의하고 /schools/ POST API를 만드세요.
#
# Student 필드: name(str, 최대 10자), grade(int, 1~6 사이)
# School 필드: school_name(str), students(List[Student])

class Student(BaseModel):
    name: str = Field(max_length=10)
    grade: int = Field(ge=1, le=6)

class School(BaseModel):
    school_name: str
    students: List[Student]

@app.post("/schools/")
def create_school(school: School):
    return school

""" 7번 문제 """

# 7. computed_field - BMI 자동 계산
# HealthInfo 모델을 정의하고 /health/ POST API를 만드세요.
#
# 필드: name(str), height(float, cm), weight(float, kg)
# bmi는 자동 계산 (소수점 첫째자리 반올림)
# 힌트: bmi = weight / (height/100)²

class HealthInfo(BaseModel):
    name: str
    height: float = Field(description="cm")
    weight: float = Field(description="kg")

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height / 100) ** 2, 1)

@app.post("/health/")
def create_health(health: HealthInfo):
    return health

""" 8번 문제 """

# 8. field_validator - 날짜 검증
# Event 모델을 정의하고 /events/ POST API를 만드세요.
#
# 필드: title(str), start_date(datetime), end_date(datetime)
# start_date는 과거면 에러 반환
# end_date는 start_date보다 이전이면 에러 반환 (model_validator 사용)

class Event(BaseModel):
    title: str
    start_date: datetime = Field(description="시작 날짜")
    end_date: datetime = Field(description="종료 날짜")

    @field_validator("start_date")
    @classmethod
    def start_validator(cls, v):
        if v < datetime.now():
            raise ValueError("날짜를 정확히 입력해주세요.")
        return v

    @model_validator(mode="after")
    def date_validator(self):
        if self.end_date < self.start_date:
            raise ValueError("날짜를 정확히 입력해주세요.")
        return self

@app.post("/events/")
def create_event(event: Event):
    return event

""" 9번 문제"""

# 9. UUID + created_at 자동 설정
# Post 모델을 정의하고 /posts/ POST API를 만드세요.
#
# 필드: post_id(str, UUID 자동 생성), title(str), content(str), created_at(str, 현재 시간 자동 설정)

class Post(BaseModel):
    post_id: str = Field(default_factory=lambda:str(uuid.uuid4()))
    title: str
    content: str
    created_at: str = Field(default_factory=lambda:datetime.now().strftime("%y-%m-%d %H:%M:%S"))

@app.post("/posts/")
def create_post(post: Post):
    return post

""" 10번 문제 """

# 10. 소문자 변환 + 이메일 검증
# Newsletter 모델을 정의하고 /newsletter/ POST API를 만드세요.
#
# 필드: email(str), name(str)
# email 대문자를 소문자로 변환 (before)
# email 형식 검증 xxx@xxx.xxx (after, re 사용)

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

class Newsletter(BaseModel):
    email: str
    name: str

    @field_validator("email")
    @classmethod
    def email_validator(cls, v):
        v = v.lower()
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("올바른 형식으로 작성해주세요. ex) xxx@xxx.xxx")
        return v

@app.post("/newsletter/")
def create_newsletter(newsletter: Newsletter):
    return newsletter