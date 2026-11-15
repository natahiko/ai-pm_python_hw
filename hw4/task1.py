from datetime import datetime
from typing import Optional


def get_days_from_today(date: str) -> Optional[int]:
    try:
        given_date = datetime.strptime(date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        print(f"Некоректний формат дати: {date!r}. Очікується 'РРРР-ММ-ДД'.")
        return None

    today = datetime.today().date()  # тільки дата, без часу
    return (today - given_date).days


if __name__ == "__main__":
    print(get_days_from_today("2021-10-09"))
    print(get_days_from_today("2030-01-01"))
    print(get_days_from_today("09.10.2021"))  # некоректний формат
