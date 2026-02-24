from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# 비동기 SQLite (데이터 저장 주소)
DATABASE_URL = "sqlite+aiosqlite:///./test_jwt.db"

# 엔진 생성 (데이터베이스를 이걸 사용하겠다고 알림)
engine = create_async_engine(DATABASE_URL, echo=True,)

# 데이터베이스 세션 생성: db (B) <----연결 통로----> 서버 (A)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, # engine이라는 DB에 연결
    autocommit=False,
    # 자동 저장 끄기(True=켜기 이러면 db.add()하면 바로 저장됨)
    autoflush=False,
    # 자동 반영 끄기, 내가 원할 때만 반영(True=켜기 이러면 조회할 때 자동 DB에 반영)
    expire_on_commit=False,
    # 커밋 후 데이터 유지(True일 경우 커밋 후 데이터 사라짐)
)

# 데이터베이스 세부 내용 세팅
## Base 클래스 생성: python -> sql (테이블 내용. 번역기)
class Base(DeclarativeBase):
    pass

# 데이터베이스 초기화: 테이블 세팅
async def init_db():
    async with AsyncSessionLocal() as session:
        yield session