from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from typing import List
import asyncio
import uuid
import re
import random

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
        if self.ticket_type not in ["adult", "child"]
            raise ValueError("adult는 18세 이상이여야합니다.")
        else
            self.ticket_type