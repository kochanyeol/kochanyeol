from datetime import datetime

def get_eta(purchase_date: datetime) -> datetime:
    pass

def test_eta() -> None:

    purchase_date = datetime(2020, 1, 2)

    result = get_eta(purchase_date)

    assert result == datetime(2020, 1, 2)
