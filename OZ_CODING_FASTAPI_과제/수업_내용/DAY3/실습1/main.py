from sqlalchemy import String, Integer, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import asyncio


# 비동기 SQLite (데이터 저장 주소)
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# 엔진 생성 (데이터베이스를 이걸 사용하겠다고 알림)
engine = create_async_engine(DATABASE_URL, echo=True)


# 데이터베이스 세부 내용 세팅
## Base 클래스 생성: python -> sql (테이블 내용. 번역기)
class Base(DeclarativeBase):
    pass


## 모델 정의: db에 들어갈 테이블 정의
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)


# 데이터베이스 초기화: 테이블 세팅
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# 데이터베이스 세션 생성: db (B) <----연결 통로----> 서버 (A)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session


########
# CRUD
########


# 1. Create
async def create_user(name: str, email: str):
    async with AsyncSessionLocal() as db:  # 데이터베이스 연결
        new_user = User(name=name, email=email)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user


# 2. Read
## 전체
async def get_all_users():
    async with AsyncSessionLocal() as db:
        result = await db.execute(text("SELECT * FROM users"))
        users = result.fetchall()
        return users


## 특정
async def get_user_by_email(email: str):
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            text("SELECT * FROM users WHERE email = :email"), {"email": email}
        )
        user = result.fetchone()
        return user


# 3. Update
async def update_user(user_id: int, name: str, email: str):
    async with AsyncSessionLocal() as db:
        user = await db.get(User, user_id)
        if not user:
            return None

        user.name = name
        user.email = email
        await db.commit()
        await db.refresh(user)
        return user


# 4. Delete
async def delete_user(user_id: int):
    async with AsyncSessionLocal() as db:
        user = await db.get(User, user_id)
        if not user:
            return None
        db.delete(user)
        await db.commit()
        return user_id


if __name__ == "__main__":

    async def main():
        await init_db()

        # 사용자 생성
        user1 = await create_user(name="김민석", email="msk@oz.com")
        user2 = await create_user(name="오디모데", email="odmd@oz.com")
        print(user1, user2)

        # 모든 사용자 조회
        users = await get_all_users()
        for user in users:
            print(user)

        # 특정 사용자
        user = await get_user_by_email(email="msk@oz.com")
        print(user)

        # 사용자 수정
        updated_user = await update_user(
            user_id=user2.id, name="진짜오디모데", email="real_odmd@oz.com"
        )
        print(updated_user)

        # 사용자 삭제
        deleted_id = await delete_user(user_id=user1.id)
        print(deleted_id)

    asyncio.run(main())