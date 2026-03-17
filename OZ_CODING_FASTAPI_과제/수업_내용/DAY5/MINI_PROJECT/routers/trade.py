"""
거래 라우터 (Trade Router)
- 사용자 자산 상태 조회 및 매수/매도 로직 처리
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from ..auth import get_current_user
from .. import models
from .. import schemas
from market import manager

router = APIRouter()

@router.get("/user/status")
async def get_status(
    current_price: float,
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """사용자 자산 상태 조회 실습"""

    # db.execute와 select를 사용해 현재 유저의 Portfolio 정보를 조회하세요
    # 유저 아이디 user.username
    result = await db.execute(select(models.Portfolio).where(models.Portfolio.username == user.username))
    p = result.scalar_one_or_none()

    # 포트폴리오(p) 존재 여부에 따라 보유수량(amount)과 평단가(avg_price)를 변수에 저장하세요 (없으면 0)
    amount = p.amount if p else 0

    avg_price = p.avg_price if p else 0

    # 현재가(current_price)를 기준으로 다음 수치를 계산하세요
    # 1. evaluation: 평가 금액 (보유수량 * 현재가)
    # 2. profit: 평가 손익 (평가 금액 - 투자 원금)
    evaluation = amount * current_price
    profit = evaluation - (amount * avg_price)

    # 힌트: 투자 원금은 (보유수량 * 평단가) 입니다.

    # 계산된 정보를 바탕으로 다음 키를 가진 딕셔너리를 반환하세요
    # 반환 키: "cash", "holdings", "evaluation", "profit", "total_asset"
    return {
        "cash": user.balance,
        "holdings": amount,
        "avg_price": avg_price,
        "evaluation": evaluation,
        "profit": profit,
        "total_asset": user.balance + evaluation
    }


@router.post("/trade/{action}")
async def trade(
    action: str,
    payload: schemas.TradeRequest,
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """매수 및 매도 처리 로직 실습"""

    username = user.username
    # DB에서 해당 유저의 포트폴리오 정보를 조회하세요 (변수명: p)
    result = await db.execute(
        select(models.Portfolio).where(
            models.Portfolio.username == username, models.Portfolio.symbol == "SAMSUNG"
        )
    )

    p = result.scalar_one_or_none()

    if action == "buy":
        # 총 매수 비용(cost)을 계산하고, 유저 잔액(user.balance)이 부족할 경우 HTTPException(400)을 발생시키세요.
        cost = payload.amount * payload.price
        if user.balance < cost:
            raise HTTPException(status_code=400, detail='잔액이 부족합니다.')

        # 유저의 잔액에서 매수 비용을 차감하세요.
        user.balance -= cost

        # 포트폴리오 업데이트 로직을 구현하세요.
        if p:
            total_cost = p.amount * p.price + cost
            p.amount += payload.amount
            p.avg_price = total_cost / p.amount
        # 1. 기존 데이터(p)가 있는 경우: 가중 평균을 이용해 평단가(p.avg_price)를 갱신하고 수량을 더합니다.

        else:
            new_p = models.Portfolio(
                username=username,
                symbol='SAMSUNG',
                amount=payload.amount,
                avg_price=payload.price
            )
            db.add(new_p)
        # 2. 기존 데이터가 없는 경우: 새로운 models.Portfolio 객체를 생성(new_p)하고 db.add() 하세요.


    elif action == "sell":
        # 매도 가능 여부를 체크하세요. (포트폴리오가 없거나, 보유 수량 < 매도 요청 수량일 경우 400 에러)
        if not p or p.amount < payload.amount:
            raise HTTPException(status_code=400, detail='보유 수량을 확인해주세요.')

        user.balance += payload.amount * payload.price
        p.amount -= payload.amount
        # 유저의 잔액을 매도 대금만큼 증가시키고, 포트폴리오 수량(p.amount)을 차감하세요.

        if p.amount == 0:
            await db.delete(p)
        # 수량이 0이 될 경우 db.delete(p)를 호출하여 데이터를 삭제하세요.

    await db.commit()
    # db.commit()으로 변경 사항을 저장하세요.

    await manager.broadcast({
        "type": "trade_news",
        "msg": f"🔔 {username}님 {action} 완료"
    })
    # manager.broadcast를 사용해 전체 사용자에게 거래 알림 메시지를 전송하세요.
    # 메시지 형식: {"type": "trade_news", "msg": f"🔔 {username}님 {action} 완료"}

    return {"msg": "success"}