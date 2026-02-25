"""
DB 모델 (Models Layer)
- SQLAlchemy 테이블 정의
"""

from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class User(Base):
    """사용자 테이블"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    balance: Mapped[float] = mapped_column(Float, default=3000000)
    # id, username(아이디), password(암호화된 비번), balance(잔액, float) 필드를 정의하세요

class Portfolio(Base):
    """포트폴리오 테이블"""
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False) #FK
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, default=0)
    avg_price: Mapped[float] = mapped_column(Float, default=0)

    # id, username(소유자 아이디), symbol(종목코드), amount(보유수량), avg_price(매수평단가) 필드를 정의하세요