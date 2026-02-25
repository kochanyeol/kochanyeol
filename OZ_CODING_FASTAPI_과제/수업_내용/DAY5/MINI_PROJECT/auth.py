"""
보안 및 인증 (Authentication Layer)
- 비밀번호 해싱 및 JWT 토큰 검증 처리
"""

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
import models
from datetime import datetime, timedelta

# JWT 서명에 사용할 SECRET_KEY와 ALGORITHM(HS256)을 설정하세요
SECRET_KEY = "ozbe17_super_long_and_complicate_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINS = 15

# 비밀번호 암호화 컨텍스트 (argon2 알고리즘 사용)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# 토큰 추출을 위한 OAuth2 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)
    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    """토큰 해독 후 현재 로그인한 유저 정보를 반환하는 의존성 함수"""
    try:
        # jwt.decode를 사용하여 토큰을 해독하고 유저네임(sub)을 추출하세요
        # DB에서 해당 유저를 조회(select)하여 변수 user에 저장하세요
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 알고리즘은 리스트로
        # 이름은 그냥 payload가 국룰, 파이썬을 위해 딕셔너리 형태로 반환된다

        username: str = payload.get("sub")
        result = await db.execute(select(models.User).where(models.User.username == username))
        user = result.scalar_one_or_none()

        # 유저가 존재하지 않을 경우 401 에러 발생
        if user is None:
            raise HTTPException(status_code=401, detail="존재하지 않는 유저")

        return user

    # 토큰 무효화 등 예외 발생 시 401 에러 반환
    except JWTError:
        raise HTTPException(status_code=401, detail='유효하지 않은 토큰')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="예상치 못한 오류 발생")