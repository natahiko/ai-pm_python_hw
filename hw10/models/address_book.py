from collections import UserDict
from datetime import date, timedelta
from typing import Optional

from .fields import DATE_FORMAT
from .record import Record


# 29.02 у невисокосний рік -> 28.02
def _birthday_in_year(birthday: date, year: int) -> date:
    try:
        return birthday.replace(year=year)
    except ValueError:
        return birthday.replace(year=year, day=28)


# Ключ — ім'я, значення — Record
class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        self.data.pop(name, None)

    # Вихідні переносимо на понеділок
    def get_upcoming_birthdays(self, days: int = 7) -> list[dict]:
        today = date.today()
        upcoming = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = _birthday_in_year(record.birthday.value, today.year)
            if birthday < today:  # вже минув
                birthday = _birthday_in_year(record.birthday.value, today.year + 1)

            if (birthday - today).days < days:
                # 5 — субота, 6 — неділя
                if birthday.weekday() == 5:
                    birthday += timedelta(days=2)
                elif birthday.weekday() == 6:
                    birthday += timedelta(days=1)

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": birthday.strftime(DATE_FORMAT),
                })

        return upcoming
