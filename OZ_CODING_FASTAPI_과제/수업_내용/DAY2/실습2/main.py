from fastapi import FastAPI
from pydantic import BaseModel, field_validator, Field
from datetime import datetime, timezone

app = FastAPI()

class Reservation(BaseModel):
    name: str = Field(..., max_length=50, description="이름 길이 50자 이내 작성")
    email: str = Field(..., description="이메일 입력하세요")
    date: datetime
    special_requests: str = Field(default="", description="옵션 요청 입력")

    # @field_validator("name")
    # @classmethod
    # def validate_name_length(cls, value: str):
    #     if len(value) > 50:
    #         raise ValueError("이름은 50자를 초과하면 안됩니다")
    #     return value

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: datetime):
        if value < datetime.now(timezone.utc): # 과거시간
            raise ValueError("과거 날짜입니다")
        return value


@app.post("/reservations/")
def create_reservation(reservation: Reservation):
    return {"reservation": reservation}