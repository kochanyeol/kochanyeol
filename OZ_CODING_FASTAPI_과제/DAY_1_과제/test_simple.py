from datetime import datetime, timedelta

# 배송일을 상수로 표현하여 이해하기 쉽게 정의
DELIVERY_DAYS = 2

# _내부에서만 함수를 사용할거다(관례)
# 휴일의 day를 datetime type으로 하고 bool으로 반환할거다
def _is_holiday(day: datetime) -> bool:
    # 일요일은 6만 해당한다 이로인해 우리는 토요일(5)까지 False로 반환할것이다
    # 왜냐하면 토요일까지를 근무일로 지정할 것이기 때문에
    # 쉽게 5보다 큰 day.weekday은 일요일(6)밖에 없어 True만 반환한다.
    return day.weekday() > 5

# 주문 날짜 또한 datetime으로 받을 것이다.
def get_eta(purchase_date: datetime) -> datetime:
    # 현재 날짜를 주문 날짜로 지정
    current_date = purchase_date
    # 남은 배송일 수를 배송일로 지정
    remaining_days = DELIVERY_DAYS

    # 반복문을 통해 배송일 수가 0이 될 때까지 반복
    while remaining_days > 0:
        # 현재 날짜에서 하루씩 더한다(timedelta(days=1))
        current_date += timedelta(days=1)
        # 현재 날짜가 평일일 경우 휴일함수가 False(평일)에서 if not으로 인해 True
        if not _is_holiday(current_date):
            remaining_days -= 1

    return current_date


def test_get_eta_2023_12_01() -> None:
    result = get_eta(datetime(2023, 12, 1))
    assert result == datetime(2023, 12, 4)


def test_get_eta_2024_12_31() -> None:
    """
    공휴일 정보가 없어서 1월 1일도 평일로 취급됩니다.
    """
    result = get_eta(datetime(2024, 12, 31))
    assert result == datetime(2025, 1, 2)


def test_get_eta_2024_02_28() -> None:
    result = get_eta(datetime(2024, 2, 28))
    assert result == datetime(2024, 3, 1)


def test_get_eta_2023_02_28() -> None:
    result = get_eta(datetime(2023, 2, 28))
    assert result == datetime(2023, 3, 2)
