from fastapi import FastAPI
from pydantic import BaseModel, model_validator, EmailStr
import re

app = FastAPI()

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

class ContactInfo(BaseModel):
    email: EmailStr | None = None
    phone_number: str | None = None

    # BEFORE: 입력 데이터 전처리
    @model_validator(mode="before")
    @classmethod
    def preprocess_email(cls, data):
        if isinstance(data, dict) and data.get("email"):
            data["email"] = data["email"].lower()
        return data

    # AFTER: 비즈니스 로직 처리
    @model_validator(mode="after")
    def validate_contact_info(self):
        if not self.email and not self.phone_number:
            raise ValueError("email과 phone_number 중 하나는 입력되어야합니다")

        if self.email and not re.match(EMAIL_REGEX, self.email):
            raise ValueError("email 포맷이 아닙니다")

        return self


@app.post("/contact")
def create_contact(contact: ContactInfo):
    return {
        "message": "Contact info accepted",
        "data": contact
    }