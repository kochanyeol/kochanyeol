# [문제] Flight 모델 정의하기
#
# 필수 필드
# passenger_name: 탑승자 이름 (최대 30자)
# passport_number: 여권번호 (정확히 9자리 숫자)
# departure_date: 출발 날짜 (오늘 이후 날짜만 허용)
#
# 선택적 필드
# meal_preference: 식사 선택 (기본값: "standard")
# seat_number: 좌석 번호 (기본값: 빈 문자열)
#
# /flights/ 로 POST 요청을 받아 항공권 예약 데이터를 생성하는 API 작성

from pydantic import BaseModel, Field, model_validator, field_validator
from fastapi import FastAPI
from datetime import datetime
import re

app = FastAPI()

class Reservation(BaseModel):
    passenger_name: str = Field(max_length=30, description="최대 30자")
    passport_number: str = Field(description="9자 입력")
    departure_date: datetime
    meal_preference: str = "standard"
    seat_number: str | None = None

    @field_validator("passport_number")
    @classmethod
    def passport_number_validator(cls, v):
        if not re.match(r"^\d{9}$", v): # 9자와 숫자로 고정해주는 로직(정규패턴식)
            raise ValueError("Passport number must be 9")
        return v

    @field_validator("departure_date")
    @classmethod
    def departure_date_validator(cls, v):
        if v <= datetime.now():
            raise ValueError("Departure date must be in the future")
        return v


@app.post("/flights")
def create_reservation(reservation: Reservation):
    return reservation
