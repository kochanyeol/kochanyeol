""" 1번 문제"""

# 1. 기본 모델 정의
# Book 모델을 정의하고 /books/ POST API를 만드세요.
#
# 필드: title(str), author(str), price(float), is_available(bool, 기본값: True)

from fastapi import FastAPI
from pydantic import BaseModel, Field

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
def get_product(product_id: int):
    pass