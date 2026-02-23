""" 1번 문제"""

# 1. 기본 모델 정의
# Book 모델을 정의하고 /books/ POST API를 만드세요.
#
# 필드: title(str), author(str), price(float), is_available(bool, 기본값: True)

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from typing import List
import asyncio
import uuid

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    price: float
    is_available: bool = True

@app.post("/books/")
def create_book(book: Book):
    return book

""" 2번 문제"""

# 2. 필드 제한
# Member 모델을 정의하고 /members/ POST API를 만드세요.
#
# 필드: name(str, 최대 20자), age(int, 0 이상), email(str)

class Member(BaseModel):
    name: str = Field(max_length=20)
    age: int = Field(ge=0)
    email: str

@app.post("/members/")
def create_member(member: Member):
    return member

""" 3번 문제"""

# 3. 기본값 설정
# Comment 모델을 정의하고 /comments/ POST API를 만드세요.
#
# 필드: content(str), likes(int, 기본값: 0), is_public(bool, 기본값: True)

class Comment(BaseModel):
    content: str
    likes: int = 0
    is_public: bool = True

@app.post("/comments/")
def create_comment(comment: Comment):
    return comment

""" 4번 문제"""

# 4. 중첩 모델
# Address와 Person 모델을 정의하고 /people/ POST API를 만드세요.
#
# Address 필드: city(str), zip_code(str)
# Person 필드: name(str), address(Address)

class Address(BaseModel):
    city: str
    zip_code: str

class Person(BaseModel):
    name: str
    address: Address

@app.post("/people/")
def create_people(people: Person):
    return people

""" 5번 문제"""

# 5. List 사용
# Team과 Player 모델을 정의하고 /teams/ POST API를 만드세요.
#
# Player 필드: name(str), number(int)
# Team 필드: team_name(str), players(List[Player])

class Player(BaseModel):
    name: str
    number: int

class Team(BaseModel):
    team_name: str
    players: List[Player]

@app.post("/teams/")
def create_team(team: Team):
    return team

""" 6번 문제"""

# 6. 쿼리 매개변수
# /products/{product_id} GET API를 만드세요.
#
# product_id는 경로 매개변수
# show_detail(bool, 기본값: False)은 쿼리 매개변수
# show_detail이 True면 {"product_id": id, "detail": "상세정보"} 반환

@app.get("/products/{product_id}")
def get_product(product_id: int, show_detail: bool = False):
    if show_detail:
        return {"product_id": product_id, "detail": "상세정보"}
    return {"product_id": product_id}

""" 7번 문제"""

# 7. field_validator 기초
# Score 모델을 정의하고 /scores/ POST API를 만드세요.
#
# 필드: name(str), score(int)
# score는 0~100 사이만 허용 (field_validator 사용)

class Score(BaseModel):
    name: str
    score: int

    @field_validator("score")
    @classmethod
    def check_score(cls, v):
        if not 0 <= v <= 100:
            raise ValueError("Score must be between 0 and 100")
        return v

@app.post("/scores/")
def create_scores(scores: Score):
    return scores

""" 8번 문제"""

# 8. 선택적 필드
# Profile 모델을 정의하고 /profiles/ POST API를 만드세요.
#
# 필드: username(str), bio(str, 기본값: 빈 문자열), website(str | None, 기본값: None)

class Profile(BaseModel):
    username: str
    bio: str = ""
    website: str | None = None

@app.post("/profiles/")
def create_profile(profile: Profile):
    return profile

""" 9번 문제"""

# 9. 비동기 처리
# /async-hello/ GET API를 만드세요.
#
# 3초 지연 후 {"message": "Hello, Async World!"} 반환 (asyncio 사용)

@app.get("/async-hello/")
async def async_hello():
    await asyncio.sleep(3)
    return {"message": "Hello, Async World!"}

""" 10번 문제"""

# 10. 기본 UUID
# Item 모델을 정의하고 /items/ POST API를 만드세요.
#
# 필드: item_id(str, UUID 자동 생성), name(str), quantity(int, 1 이상)

class Item(BaseModel):
    item_id: str = Field(default_factory=lambda:str(uuid.uuid4())) # lambda는 간단한 함수로 def를 사용한 함수보다 가볍고 재사용가능
    name: str
    quantity: int = Field(gt=0) # (ge=1)

@app.post("/items/")
def create_items(item: Item):
    return item