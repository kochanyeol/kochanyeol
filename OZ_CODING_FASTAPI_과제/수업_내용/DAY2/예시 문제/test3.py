# [문제] SNS 계정 등록 모델 정의하기
#
# 요구사항
# instagram 또는 twitter 중 하나 이상 필수 입력
# instagram은 올바른 형식 사용 @username
# 만약 @ 없이 입력했을 시 자동으로 @ 추가
# twitter는 올바른 형식 사용 @username
# 대문자가 있을 시 소문자로 변환
#
#
# /sns/ 로 POST 요청을 받아 SNS 계정 데이터를 생성하는 API 작성
#
# 힌트:
# @ 자동 추가 → mode="before" + 문자열 조건 처리
# 소문자 변환 → v.lower()
# 하나 이상 필수 → model_validator

from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator

app = FastAPI()

SNS_REGEX = r"^@[a-zA-Z]+$"

class Sns(BaseModel):
    instagram: str | None = None
    twitter: str | None = None

    @model_validator(mode="before")
    @classmethod
    def preprocess_sns(cls, v):


@app.post("/sns/")
def create_sns(sns: Sns):
    return sns