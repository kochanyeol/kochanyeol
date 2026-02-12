from datetime import datetime, timedelta

DELIVERY_DATE = 2

def get_eta(purchase_date: datetime) -> datetime:
    return day.weekday() >= 5

def test_eta() -> None:

    purchase_date = datetime(2020, 1, 2)

    result = get_eta(purchase_date)

    assert result == datetime(2020, 1, 2)
