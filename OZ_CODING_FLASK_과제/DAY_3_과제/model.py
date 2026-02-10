from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
# 파이썬에서 DB를 다루는 다이어리 SQL을 직접 쓰지 않고 파이썬에서 DB를 다룸
# create_engine은 DB와 실제로 연결해주는 엔진(규칙)
from sqlalchemy.orm import declarative_base, sessionmaker
# orm은 DB의 테이블,행과 파이썬의 클래스,객체를 연결
# declarative_base는 관계형 데이터베이스의 테이블을 파이썬 객체(클래스)로 매핑하여 SQL 없이 객체처럼 데이터를 다룰 수 있게 해주는 기술
# create_engine이걸로 DB와 연결을 했으면 sessionmaker이걸로 DB와 작업통로를 찍어낸다.

""" 모델 정의 """

Base = declarative_base()
# ORM 모델을 정의하기 위한 공통 부모 클래스(Base)를 생성하는 함수
# 이 Base를 상속받는 클래스는 전부 DB 테이블이다.
class User(Base):
# 이 클래스는 orm테이블이다 선언.
    __tablename__ = 'users'
    # MODEL 정의하기

    id = Column(Integer, primary_key=True, index=True)
    # index=True는 검색 속도 향상용 인덱스를 생성하는 것
    name = Column(String, nullable=False)
    # nullable=False == not null

    def __repr__(self):
        return f'<User(id={self.id}, name={self.name})>'
    # repr은 디버깅용으로 없다면 <__main__.User object at 0x000001F...>으로 보일것이고,
    # 있다면 <User(id=1, name=OZ_BE)>로 보인다