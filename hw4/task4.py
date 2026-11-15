from datetime import date, datetime, timedelta
from typing import Dict, List


def _birthday_in_year(birthday: date, year: int) -> date:
    try:
        return birthday.replace(year=year)
    except ValueError:
        return birthday.replace(year=year, day=28)


def get_upcoming_birthdays(users: List[Dict]) -> List[Dict]:
    today = datetime.today().date()
    upcoming = []

    for user in users:
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()

        birthday_this_year = _birthday_in_year(birthday, today.year)
        if birthday_this_year < today:  # вже минув - беремо наступний рік
            birthday_this_year = _birthday_in_year(birthday, today.year + 1)

        days_until = (birthday_this_year - today).days
        if 0 <= days_until <= 6:
            congratulation_date = birthday_this_year
            # weekday(): 5 - субота, 6 - неділя
            if congratulation_date.weekday() == 5:
                congratulation_date += timedelta(days=2)
            elif congratulation_date.weekday() == 6:
                congratulation_date += timedelta(days=1)

            upcoming.append({
                "name": user["name"],
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
            })

    return upcoming


if __name__ == "__main__":
    users = [
        {"name": "John Doe", "birthday": "1985.01.23"},
        {"name": "Jane Smith", "birthday": "1990.01.27"},
    ]
    upcoming_birthdays = get_upcoming_birthdays(users)
    print("Список привітань на цьому тижні:", upcoming_birthdays)
